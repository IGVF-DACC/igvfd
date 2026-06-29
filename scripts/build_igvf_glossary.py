#!/usr/bin/env python3
"""
Build a glossary JSON from:
  - preferred_assay_titles enum_descriptions (mixins.json)
  - Software.name -> Software.description (IGVF Data Portal search API)
  - File ``file.output_types`` glossary: enum_descriptions merged from ``content_type``
    on all ``*_file.json`` profiles (same vocabulary as AnalysisStep output_content_types)
  - BioGRID experimental evidence codes (physical and genetic interaction systems)
    from the BioGRID wiki, stored in ``scripts/biogrid_experimental_systems.json``
  - IGVF Catalog OpenAPI (``scripts/catalog_api_openapi.json`` or fetched from the
    dev catalog host): string ``enum`` values for the query filter named ``method``
    are unioned across endpoints; any missing from ``preferred_assay_titles`` or
    ``software`` get ``FIX ME`` (see ``merge_catalog_openapi_enum_placeholders``).
  - File ``content_type_fields``: field names and descriptions parsed from file format
    specification Document attachments linked to IGVF catalog files, keyed by
    ``File.content_type`` (see ``scripts/igvf_catalog_content_type_to_ffs.json``).
    When multiple specifications apply to one ``content_type`` and map to distinct
    IGVF Catalog ``method`` filter values, fields are nested under those method keys.

The enabled Cursor MCP servers do not expose portal DB search; this uses the
public API (same objects as https://data.igvf.org/).

Optional: ``pip install pypdf`` improves extraction from PDF attachments.
"""

from __future__ import annotations

import importlib.util
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "src/igvfd/schemas"
MIXINS_PATH = REPO_ROOT / "src/igvfd/schemas/mixins.json"
SOFTWARE_SEARCH_URL = (
    "https://api.data.igvf.org/search/"
    "?type=Software&field=name&field=description&format=json&limit=all"
)
DOCUMENT_FFS_SEARCH_URL = (
    "https://api.data.igvf.org/search/"
    "?type=Document&document_type=file%20format%20specification"
    "&field=uuid&field=aliases&field=attachment&format=json&limit=all"
)
API_HOST = "https://api.data.igvf.org"
DEFAULT_OUTPUT = REPO_ROOT / "igvf_field_glossary.json"
BIOGRID_SYSTEMS_PATH = Path(__file__).resolve().parent / "biogrid_experimental_systems.json"
BIOGRID_SYSTEMS_SOURCE_URL = (
    "https://wiki.thebiogrid.org/doku.php/experimental_systems"
)
CATALOG_OPENAPI_CACHE = Path(__file__).resolve().parent / "catalog_api_openapi.json"
CATALOG_OPENAPI_URL = "https://api-dev.catalog.igvf.org/openapi"
CATALOG_CONTENT_TYPE_TO_FFS_PATH = (
    Path(__file__).resolve().parent / "igvf_catalog_content_type_to_ffs.json"
)
# Enum strings that appear only on these paths are regulatory-element class labels
# in the catalog API; other catalog enums default to the software glossary bucket.
_CATALOG_GE_ENUM_PATHS = frozenset({"/genomic-elements", "/genomic-elements/genes"})

_FFS_PARSERS = None


def _load_ffs_parsers():
    global _FFS_PARSERS
    if _FFS_PARSERS is not None:
        return _FFS_PARSERS
    mod_path = Path(__file__).resolve().parent / "ffs_document_parsers.py"
    spec = importlib.util.spec_from_file_location("ffs_document_parsers", mod_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load parser module from {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _FFS_PARSERS = mod
    return mod


def load_preferred_assay_glossary() -> dict[str, str]:
    with MIXINS_PATH.open(encoding="utf-8") as f:
        mixins = json.load(f)
    items = mixins["preferred_assay_titles"]["preferred_assay_titles"]["items"]
    desc = items.get("enum_descriptions") or {}
    if not isinstance(desc, dict):
        raise SystemExit("mixins.json: expected items.enum_descriptions object")
    return dict(sorted(desc.items(), key=lambda kv: kv[0].lower()))


def fetch_software_glossary() -> dict[str, str]:
    req = urllib.request.Request(
        SOFTWARE_SEARCH_URL,
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Software search failed: HTTP {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Software search failed: {e.reason}") from e

    graph = payload.get("@graph") or []
    out: dict[str, str] = {}
    duplicates: list[str] = []
    for row in graph:
        name = row.get("name")
        if not name:
            continue
        desc = row.get("description")
        if name in out:
            duplicates.append(name)
        out[str(name)] = desc if isinstance(desc, str) else ""
    if duplicates:
        print(
            f"warning: duplicate software.name entries ({len(duplicates)}); "
            "last description wins",
            file=sys.stderr,
        )
    return dict(sorted(out.items(), key=lambda kv: kv[0].lower()))


def _collect_enum_descriptions_in_subtree(node: Any) -> dict[str, str]:
    """Gather every enum_descriptions map nested under a schema subtree."""
    found: dict[str, str] = {}

    def walk(n: Any) -> None:
        if isinstance(n, dict):
            ed = n.get("enum_descriptions")
            if isinstance(ed, dict):
                for k, v in ed.items():
                    if isinstance(k, str) and isinstance(v, str):
                        found[k] = v
            for child in n.values():
                walk(child)
        elif isinstance(n, list):
            for item in n:
                walk(item)

    walk(node)
    return found


def _file_schema_merge_order(path: Path) -> tuple[int, str]:
    """Process tabular_file last so shared content_type terms get tabular definitions."""
    name = path.name
    if name == "tabular_file.json":
        return (2, name)
    if name == "reference_file.json":
        return (1, name)
    return (0, name)


def load_file_content_type_glossary() -> dict[str, str]:
    """
    Merge content_type enum_descriptions from all *File JSON schemas.

    Only ``properties.content_type`` is used (canonical submitter-facing
    definition), not conditional branches under dependentSchemas.
    Later files in the merge order overwrite duplicate keys (tabular_file last).
    """
    merged: dict[str, str] = {}
    paths = sorted(
        SCHEMAS_DIR.glob("*_file.json"),
        key=_file_schema_merge_order,
    )
    for schema_path in paths:
        with schema_path.open(encoding="utf-8") as f:
            schema = json.load(f)
        props = schema.get("properties")
        if not isinstance(props, dict):
            continue
        ct = props.get("content_type")
        if not isinstance(ct, dict):
            continue
        part = _collect_enum_descriptions_in_subtree(ct)
        merged.update(part)
    return dict(sorted(merged.items(), key=lambda kv: kv[0].lower()))


def fetch_file_format_specification_glossary() -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Download every released/public Document with document_type file format specification,
    parse attachments, return (glossary_fragment, stats).
    """
    mod = _load_ffs_parsers()
    req = urllib.request.Request(
        DOCUMENT_FFS_SEARCH_URL,
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Document search failed: HTTP {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Document search failed: {e.reason}") from e

    graph = payload.get("@graph") or []
    by_uuid: dict[str, Any] = {}
    stats = {
        "document_search_total": payload.get("total"),
        "documents_in_response": len(graph),
        "attachments_parsed": 0,
        "attachments_with_fields": 0,
        "download_failures": 0,
        "missing_attachment_metadata": 0,
        "skipped_non_text_attachment": 0,
        "skipped_pdf_no_text_extractor": 0,
        "empty_field_parse": 0,
    }

    for row in graph:
        uuid = row.get("uuid")
        att = row.get("attachment") or {}
        fn = att.get("download")
        if not uuid or not fn:
            stats["missing_attachment_metadata"] += 1
            continue
        url = (
            f"{API_HOST}/documents/{uuid}/@@download/attachment/"
            f"{urllib.parse.quote(fn, safe='')}"
        )
        try:
            dreq = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(dreq, timeout=120) as r:
                raw = r.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            print(f"warning: download failed {uuid} {fn}: {e}", file=sys.stderr)
            stats["download_failures"] += 1
            continue

        stats["attachments_parsed"] += 1
        text = mod.extract_text_from_attachment(raw, fn)
        lower = fn.lower()
        if text is None:
            if lower.endswith(".pdf"):
                stats["skipped_pdf_no_text_extractor"] += 1
            else:
                stats["skipped_non_text_attachment"] += 1
            fields: dict[str, str] = {}
        else:
            fields = mod.parse_file_format_specification_text(text)

        if fields:
            stats["attachments_with_fields"] += 1
        else:
            stats["empty_field_parse"] += 1

        aliases = row.get("aliases")
        if not isinstance(aliases, list):
            aliases = []
        by_uuid[str(uuid)] = {
            "attachment": fn,
            "aliases": aliases,
            "fields": dict(sorted(fields.items(), key=lambda kv: kv[0].lower())),
        }

    return {"by_document_uuid": by_uuid}, stats


_PLAUSIBLE_FIELD_NAME = re.compile(
    r"^(?:\{[a-zA-Z_]+\}\.)?[A-Za-z][A-Za-z0-9_.() <>{}]{0,79}$"
)

# Catalog OpenAPI ``method`` query values for method-specific file format specs.
FFS_DOCUMENT_CATALOG_METHOD: dict[str, str] = {
    "4d4f377d-ac1a-48d7-b18c-30bd601b6c61": "MutPred2",
    "8dc57d71-ff1e-4a9b-a069-7b1a68e1cbec": "ESM-1v",
    "c32ac0bf-7e94-4b56-9c80-fb62a849bd68": "VAMP-seq",
    "691b75ab-48e4-441f-bca3-b5988322a031": "SGE",
    "9d0ad6fb-777c-4cb6-a1c4-8ff7a41b17a1": "Variant-EFFECTS",
    "9e7bbb38-7412-4f0d-97e5-cd183d307485": "BlueSTARR",
    "a61b28ae-0d57-49e4-b56e-00acbad6330a": "BlueSTARR",
}


def _is_plausible_field_name(name: str) -> bool:
    return bool(_PLAUSIBLE_FIELD_NAME.match(name))


def _clean_parsed_field_description(field_name: str, description: str) -> str:
    """Drop duplicated ``field<TAB>description`` values from loose parsers."""
    desc = description.strip()
    if "\t" in desc:
        left, right = desc.split("\t", 1)
        if left.strip() == field_name:
            return right.strip()
    return desc


def build_file_content_type_fields_from_catalog_ffs() -> tuple[
    dict[str, dict[str, str] | dict[str, dict[str, str]]], dict[str, Any]
]:
    """
    Parse file format specification attachments for catalog-linked documents.

    Returns ``{content_type: {field_name: description}}`` for most types, or
    ``{content_type: {catalog_method: {field_name: description}}}`` when every
    linked specification for that type maps to a catalog ``method`` value
    (e.g. ``coding variant effects`` → ESM-1v, MutPred2, VAMP-seq).

    Document membership per ``content_type`` comes from
    ``igvf_catalog_content_type_to_ffs.json`` (IGVF_catalog_v1.1 / v1.2 files).
    """
    if not CATALOG_CONTENT_TYPE_TO_FFS_PATH.is_file():
        raise SystemExit(
            f"missing {CATALOG_CONTENT_TYPE_TO_FFS_PATH}; "
            "build igvf_catalog_content_type_to_ffs.json first"
        )
    with CATALOG_CONTENT_TYPE_TO_FFS_PATH.open(encoding="utf-8") as f:
        mapping = json.load(f)

    mod = _load_ffs_parsers()
    stats: dict[str, Any] = {
        "mapping_source": str(CATALOG_CONTENT_TYPE_TO_FFS_PATH.relative_to(REPO_ROOT)),
        "unique_documents": 0,
        "attachments_parsed": 0,
        "attachments_with_fields": 0,
        "download_failures": 0,
        "skipped_pdf_no_text_extractor": 0,
        "skipped_non_text_attachment": 0,
        "empty_field_parse": 0,
        "field_name_conflicts": 0,
        "content_types_scoped_by_method": 0,
        "content_types_with_fields": 0,
        "total_field_entries": 0,
    }

    fields_by_document_uuid: dict[str, dict[str, str]] = {}
    documents = mapping.get("documents") or []
    stats["unique_documents"] = len(documents)

    for doc in documents:
        uuid = doc.get("uuid")
        fn = doc.get("attachment")
        if not uuid or not fn:
            continue
        url = (
            f"{API_HOST}/documents/{uuid}/@@download/attachment/"
            f"{urllib.parse.quote(str(fn), safe='')}"
        )
        try:
            dreq = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(dreq, timeout=120) as r:
                raw = r.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            print(
                f"warning: FFS download failed {uuid} {fn}: {e}",
                file=sys.stderr,
            )
            stats["download_failures"] += 1
            fields_by_document_uuid[str(uuid)] = {}
            continue

        stats["attachments_parsed"] += 1
        text = mod.extract_text_from_attachment(raw, str(fn))
        lower = str(fn).lower()
        if text is None:
            if lower.endswith(".pdf"):
                stats["skipped_pdf_no_text_extractor"] += 1
            else:
                stats["skipped_non_text_attachment"] += 1
            parsed: dict[str, str] = {}
        else:
            parsed = mod.parse_file_format_specification_text(text)

        cleaned = {
            k: _clean_parsed_field_description(k, v)
            for k, v in parsed.items()
            if k and v and _is_plausible_field_name(k)
        }
        fields_by_document_uuid[str(uuid)] = dict(
            sorted(cleaned.items(), key=lambda kv: kv[0].lower())
        )
        if cleaned:
            stats["attachments_with_fields"] += 1
        else:
            stats["empty_field_parse"] += 1

    by_content_type: dict[str, dict[str, str] | dict[str, dict[str, str]]] = {}
    for content_type, entry in (mapping.get("by_content_type") or {}).items():
        specs = entry.get("file_format_specifications") or []
        method_keys = [
            FFS_DOCUMENT_CATALOG_METHOD[str(spec.get("uuid") or "")]
            for spec in specs
            if str(spec.get("uuid") or "") in FFS_DOCUMENT_CATALOG_METHOD
        ]
        scope_by_method = bool(specs) and len(method_keys) == len(specs)

        if scope_by_method:
            by_method: dict[str, dict[str, str]] = {}
            for spec in specs:
                uuid = str(spec.get("uuid") or "")
                method = FFS_DOCUMENT_CATALOG_METHOD[uuid]
                fields = fields_by_document_uuid.get(uuid, {})
                if method in by_method:
                    for field_name, description in fields.items():
                        if field_name in by_method[method]:
                            if by_method[method][field_name] != description:
                                stats["field_name_conflicts"] += 1
                            continue
                        by_method[method][field_name] = description
                else:
                    by_method[method] = dict(fields)
            if by_method:
                scoped = {
                    method: dict(sorted(fields.items(), key=lambda kv: kv[0].lower()))
                    for method, fields in sorted(
                        by_method.items(), key=lambda kv: kv[0].lower()
                    )
                    if fields
                }
                if scoped:
                    by_content_type[content_type] = scoped
                stats["content_types_scoped_by_method"] += 1
            continue

        merged: dict[str, str] = {}
        for spec in specs:
            uuid = str(spec.get("uuid") or "")
            for field_name, description in fields_by_document_uuid.get(uuid, {}).items():
                if field_name in merged:
                    if merged[field_name] != description:
                        stats["field_name_conflicts"] += 1
                        print(
                            f"warning: field '{field_name}' conflict for "
                            f"content_type '{content_type}' "
                            f"(document {uuid}); keeping first definition",
                            file=sys.stderr,
                        )
                    continue
                merged[field_name] = description
        if merged:
            by_content_type[content_type] = dict(
                sorted(merged.items(), key=lambda kv: kv[0].lower())
            )

    stats["content_types_with_fields"] = len(by_content_type)

    def _entry_count(value: dict[str, str] | dict[str, dict[str, str]]) -> int:
        if not value:
            return 0
        first = next(iter(value.values()))
        if isinstance(first, dict):
            return sum(len(v) for v in value.values())  # type: ignore[arg-type]
        return len(value)

    stats["total_field_entries"] = sum(
        _entry_count(v) for v in by_content_type.values()
    )
    return dict(sorted(by_content_type.items(), key=lambda kv: kv[0].lower())), stats


def load_catalog_openapi_spec() -> dict[str, Any] | None:
    """
    Load the IGVF Catalog OpenAPI document (used for the ``method`` filter enum).

    Prefer a checked-in snapshot at ``scripts/catalog_api_openapi.json`` so builds
    stay reproducible. If missing, fetch from the dev catalog host (TLS uses the
    catalog dev certificate, which may not match ``api-dev.catalog.igvf.org`` in
    all environments, so verification is disabled only for that GET).
    """
    if CATALOG_OPENAPI_CACHE.is_file():
        with CATALOG_OPENAPI_CACHE.open(encoding="utf-8") as f:
            return json.load(f)
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(
        CATALOG_OPENAPI_URL,
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            return json.load(resp)
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        print(
            f"warning: catalog OpenAPI fetch failed ({e}); skipping enum placeholders",
            file=sys.stderr,
        )
        return None


def _openapi_method_filter_enum_value_paths(spec: dict[str, Any]) -> dict[str, set[str]]:
    """
    Map each string ``enum`` value to paths where it appears as the ``method``
    query parameter (catalog list/filter facet), not other parameters or schemas.
    """
    value_paths: dict[str, set[str]] = defaultdict(set)
    for path, path_item in (spec.get("paths") or {}).items():
        for _http_method, op in path_item.items():
            if _http_method.startswith("x-") or not isinstance(op, dict):
                continue
            for par in op.get("parameters") or []:
                if not isinstance(par, dict):
                    continue
                if par.get("name") != "method" or par.get("in") != "query":
                    continue
                sch = par.get("schema")
                if not isinstance(sch, dict):
                    continue
                en = sch.get("enum")
                if not isinstance(en, list):
                    continue
                for x in en:
                    if isinstance(x, str):
                        value_paths[x].add(path)
    return dict(value_paths)


def _catalog_enum_placeholder_section(paths: set[str]) -> str:
    if paths <= _CATALOG_GE_ENUM_PATHS:
        return "preferred_assay_titles"
    return "software"


def merge_catalog_openapi_enum_placeholders(
    preferred_assay: dict[str, str],
    software: dict[str, str],
) -> tuple[dict[str, str], dict[str, str], dict[str, Any]]:
    """
    For every string ``enum`` on the catalog ``method`` query filter, ensure the
    glossary has a definition under ``preferred_assay_titles`` or ``software``.
    Missing keys are added with the text ``FIX ME`` (placeholders for curation).
    """
    meta: dict[str, Any] = {
        "catalog_openapi_loaded": False,
    }
    spec = load_catalog_openapi_spec()
    if not spec:
        return preferred_assay, software, meta

    value_paths = _openapi_method_filter_enum_value_paths(spec)
    meta["catalog_openapi_loaded"] = True
    meta["catalog_openapi_source"] = (
        str(CATALOG_OPENAPI_CACHE.relative_to(REPO_ROOT))
        if CATALOG_OPENAPI_CACHE.is_file()
        else CATALOG_OPENAPI_URL
    )
    meta["catalog_openapi_method_filter_enum_distinct_strings"] = len(value_paths)

    pa = dict(preferred_assay)
    sw = dict(software)
    fix_pa = 0
    fix_sw = 0
    for val, paths in value_paths.items():
        if val in pa or val in sw:
            continue
        if _catalog_enum_placeholder_section(paths) == "preferred_assay_titles":
            pa[val] = "FIX ME"
            fix_pa += 1
        else:
            sw[val] = "FIX ME"
            fix_sw += 1
    meta["catalog_openapi_method_fix_me_preferred_assay_titles"] = fix_pa
    meta["catalog_openapi_method_fix_me_software"] = fix_sw
    return pa, sw, meta


def load_biogrid_experimental_systems() -> dict[str, Any]:
    """BioGRID wiki experimental evidence codes (physical and genetic interactions)."""
    with BIOGRID_SYSTEMS_PATH.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {
        "physical_interactions": dict(
            sorted(
                raw["physical_interactions"].items(),
                key=lambda kv: kv[0].lower(),
            )
        ),
        "genetic_interactions": dict(
            sorted(
                raw["genetic_interactions"].items(),
                key=lambda kv: kv[0].lower(),
            )
        ),
    }


def main() -> None:
    out_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    file_ct = load_file_content_type_glossary()
    content_type_fields, ffs_by_ct_stats = (
        build_file_content_type_fields_from_catalog_ffs()
    )
    biogrid = load_biogrid_experimental_systems()
    pa = load_preferred_assay_glossary()
    sw = fetch_software_glossary()
    pa, sw, catalog_meta = merge_catalog_openapi_enum_placeholders(pa, sw)
    doc = {
        "preferred_assay_titles": dict(
            sorted(pa.items(), key=lambda kv: kv[0].lower())
        ),
        "software": dict(sorted(sw.items(), key=lambda kv: kv[0].lower())),
        "file": {
            "output_types": file_ct,
            "content_type_fields": content_type_fields,
        },
        "biogrid_experimental_systems": biogrid,
        "_meta": {
            "preferred_assay_titles_source": str(
                MIXINS_PATH.relative_to(REPO_ROOT)
            ),
            "software_source_url": SOFTWARE_SEARCH_URL,
            "software_object_count": None,
            "file_output_types_schema_property": "content_type",
            "file_output_types_note": (
                "Values and enum_descriptions come from File.content_type on *File "
                "profiles (merged union; aligns with AnalysisStep output_content_types)."
            ),
            "file_output_types_term_count": len(file_ct),
            "file_output_types_schemas_scanned": sorted(
                {p.name for p in SCHEMAS_DIR.glob("*_file.json")}
            ),
            "file_content_type_fields_note": (
                "Parsed from file format specification Document attachments "
                "linked to IGVF catalog v1.1/v1.2 files, grouped by File.content_type. "
                "When multiple specifications map to distinct IGVF Catalog method "
                "filter values, fields are nested under those method keys."
            ),
            "file_content_type_fields_mapping": str(
                CATALOG_CONTENT_TYPE_TO_FFS_PATH.relative_to(REPO_ROOT)
            ),
            **{
                f"file_content_type_fields_{k}": v
                for k, v in ffs_by_ct_stats.items()
                if k != "mapping_source"
            },
            "biogrid_experimental_systems_source_url": BIOGRID_SYSTEMS_SOURCE_URL,
            "biogrid_experimental_systems_data_file": str(
                BIOGRID_SYSTEMS_PATH.relative_to(REPO_ROOT)
            ),
            "biogrid_physical_interaction_count": len(
                biogrid["physical_interactions"]
            ),
            "biogrid_genetic_interaction_count": len(biogrid["genetic_interactions"]),
            **catalog_meta,
        },
    }
    doc["_meta"]["software_object_count"] = len(doc["software"])
    out_path.write_text(json.dumps(doc, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
