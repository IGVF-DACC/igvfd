"""
Heuristic parsers for IGVF Document attachments with document_type
``file format specification``. Formats vary (AutoSQL, TSV headers, HTML tables, etc.).
"""

from __future__ import annotations

import html as html_module
import io
import re
from typing import Callable

_TYPE_TOKENS = frozenset(
    {
        "string",
        "str",
        "integer",
        "int",
        "uint",
        "float",
        "double",
        "boolean",
        "bool",
        "character",
        "char",
        "long",
        "short",
        "bigint",
        "object",
    }
)


def _norm_key(name: str) -> str:
    n = name.strip()
    n = re.sub(r"\s+", "_", n)
    return n


def parse_autosql(text: str) -> dict[str, str]:
    """UCSC AutoSQL-style ``type field; "description"`` inside a stanza."""
    out: dict[str, str] = {}
    for m in re.finditer(
        r'(?m)^\s*\S+\s+(\S+)\s*;\s*"((?:[^"\\]|\\.)*)"\s*$',
        text,
    ):
        field = m.group(1).strip()
        desc = m.group(2).replace("\\n", "\n").replace('\\"', '"')
        if field and desc:
            out[field] = desc
    return out


_ROW_TYPE_RE = re.compile(
    r"^([A-Za-z_][\w()]*)\s+(string|integer|float|logical)(?:\s+(.*))?$",
    re.IGNORECASE,
)


def _description_from_type_line_remainder(rest: str) -> str:
    """Drop a leading ``[possible values]`` token and return description text."""
    s = rest.strip()
    if not s:
        return ""
    if s.startswith("["):
        m = re.match(r"^\[[^\]]*\]\s*(.*)$", s, re.DOTALL)
        if m:
            return m.group(1).strip()
        return ""
    return s


def _is_possible_values_fragment(line: str) -> bool:
    """Lines that belong to the ``Possible values`` column, not ``Description``."""
    s = line.strip()
    if not s:
        return True
    if s.startswith("[") and "]" in s and not _description_from_type_line_remainder(s):
        return True
    if s.startswith("[") and "]" not in s:
        return True
    if s.endswith("]") and not re.search(r"[a-z]{4,}", s):
        return True
    return False


def parse_name_type_description_table(text: str) -> dict[str, str]:
    """
    PDF tables with header ``Name``, ``Type``, ``Possible values``, ``Description``
    (e.g. TAP-seq per-element output). pypdf flattens rows; each field starts with
    ``<name> <type>`` on its own line and the description follows until the next field.
    """
    if "possible values" not in text.lower() or "description" not in text.lower():
        return {}
    lines = [ln.strip() for ln in text.replace("\r\n", "\n").split("\n") if ln.strip()]
    start = 0
    for i, ln in enumerate(lines):
        low = ln.lower()
        if "name" in low and "type" in low and "description" in low:
            start = i + 1
            break

    out: dict[str, str] = {}
    i = start
    while i < len(lines):
        m = _ROW_TYPE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        name, _type, same_line_rest = m.group(1), m.group(2), (m.group(3) or "").strip()
        i += 1
        desc_parts: list[str] = []
        same_line_desc = _description_from_type_line_remainder(same_line_rest)
        if same_line_desc:
            desc_parts.append(same_line_desc)
        while i < len(lines) and not _ROW_TYPE_RE.match(lines[i]):
            if not _is_possible_values_fragment(lines[i]):
                desc_parts.append(lines[i])
            i += 1
        desc = re.sub(r"\s+", " ", " ".join(desc_parts)).strip()
        if name and desc and name.lower() != "name":
            out[name] = desc
    return out


def parse_column_header_table(text: str) -> dict[str, str]:
    """
    Header like ``Column Number<TAB>Name<TAB>Description`` or comma variant,
    or ``Column # | Data Type | Description`` (pipe), then one row per field.
    """
    lines = [ln.strip() for ln in text.replace("\r\n", "\n").split("\n") if ln.strip()]
    if not lines:
        return {}
    header = lines[0].lower()
    if "description" not in header or "column" not in header:
        return {}
    if "|" in lines[0] and "\t" not in lines[0]:
        delim = "|"
    else:
        delim = "\t" if lines[0].count("\t") >= 2 else ","
    hdr_cells = [c.strip().lower() for c in lines[0].split(delim)]
    data_type_style = "data type" in header and "name" not in "".join(hdr_cells)
    name_i: int | None = None
    desc_i: int | None = None
    if not data_type_style:
        try:
            name_i = next(i for i, h in enumerate(hdr_cells) if h in ("name", "column name"))
        except StopIteration:
            name_i = 1 if len(hdr_cells) > 1 else 0
        try:
            desc_i = next(i for i, h in enumerate(hdr_cells) if "description" in h)
        except StopIteration:
            desc_i = len(hdr_cells) - 1
    else:
        desc_i = len(hdr_cells) - 1
        name_i = 0

    out: dict[str, str] = {}
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(delim)]
        if len(parts) <= max(name_i, desc_i):
            continue
        if data_type_style:
            key = re.sub(r"\s+", "_", parts[0].lower())
            desc = parts[desc_i] if desc_i is not None else ""
        else:
            key = parts[name_i]
            desc = parts[desc_i]
        if not key or key.lower() == "name":
            continue
        out[_norm_key(key) if " " in key and not data_type_style else key] = desc
    return out


def parse_pipe_column_lines(text: str) -> dict[str, str]:
    """Lines like ``Column 1 | string | Description text``."""
    out: dict[str, str] = {}
    for ln in text.replace("\r\n", "\n").split("\n"):
        if "|" not in ln or "column" not in ln.lower():
            continue
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 3:
            continue
        col = parts[0]
        mid = parts[1].lower()
        desc = parts[-1]
        if not re.search(r"column\s*#?\s*\d+", col, re.I):
            continue
        if mid in _TYPE_TOKENS:
            key = re.sub(r"\s+", "_", col.lower())
            out[key] = desc
        else:
            out[_norm_key(mid)] = desc
    return out


def parse_html_table(text: str) -> dict[str, str]:
    """Simple ``<tr><td>…</td><td>name</td><td>desc</td>`` tables (3+ cells)."""
    out: dict[str, str] = {}
    blob = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in re.finditer(
        r"<tr[^>]*>\s*(.*?)\s*</tr>",
        blob,
        flags=re.I | re.S,
    ):
        row = m.group(1)
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.I | re.S)
        texts: list[str] = []
        for c in cells:
            t = re.sub(r"<[^>]+>", " ", c)
            t = html_module.unescape(re.sub(r"\s+", " ", t).strip())
            texts.append(t)
        if len(texts) < 3:
            continue
        # Skip header rows
        if texts[1].lower() in ("name", "column", "field"):
            continue
        name, desc = texts[1], texts[2]
        if name and desc and not name.isdigit():
            out[name] = desc
    return out


def parse_space_dash(text: str) -> dict[str, str]:
    """``FieldName    - rest is definition`` (VariantChr style)."""
    out: dict[str, str] = {}
    for ln in text.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+-\s+(.+)$", ln)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def parse_tab_kv_body(text: str) -> dict[str, str]:
    """Body lines ``field<TAB>definition`` (SCEPTRE-style); skips title / blanks."""
    out: dict[str, str] = {}
    lines = text.replace("\r\n", "\n").split("\n")
    started = False
    for ln in lines:
        raw = ln.rstrip()
        if "\t" not in raw:
            if started and not raw.strip():
                break
            continue
        left, right = raw.split("\t", 1)
        key = left.strip()
        val = right.strip()
        if not key or not val:
            continue
        if not re.match(r"^[A-Za-z_][\w]*$", key):
            continue
        started = True
        out[key] = val
    return out


def _normalize_pdf_ligatures(text: str) -> str:
    """Map common PDF ligatures to ASCII (e.g. TLand spec uses ﬂoat, ﬁle)."""
    return (
        text.replace("\ufb02", "fl")
        .replace("\ufb01", "fi")
        .replace("\ufb00", "ff")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )


def _split_type_example_description(rest: str) -> str:
    """Return the Description column text after Data type and Example columns."""
    rest = rest.strip()
    if not rest:
        return ""
    patterns = [
        r"^N/A\s+(.+)$",
        r"^chr\d+\s+(.+)$",
        r"^chr\d+:\d+-\d+\s+(.+)$",
        r"^NC_\S+\s+(.+)$",
        r"^[-\d.]+\s+(.+)$",
        r"^[GC]\s+(.+)$",
        r"^binding_\w+\s+(.+)$",
        r"^(\S{1,60})\s+(.+)$",
    ]
    for pat in patterns:
        m = re.match(pat, rest, re.DOTALL)
        if m:
            return m.group(m.lastindex).strip()
    return rest


def parse_columns_are_as_follows_colon_descriptions(text: str) -> dict[str, str]:
    """
    ESM-1v-style column glossary: ``columns are as follows:`` then
    ``{column_name}: {description}`` entries.
    """
    text = _normalize_pdf_ligatures(text)
    m = re.search(
        r"columns are as follows:\s*(.*?)(?:Model information|\Z)",
        text,
        re.I | re.DOTALL,
    )
    if not m:
        return {}
    section = re.sub(r"\s+", " ", m.group(1)).strip()
    col_re = re.compile(
        r"\b((?:GENCODE\.v\d+\.\w+|HGVS\.p|esm1v_t33_650M_UR90S_\d(?:_next)?|combined_score)):\s*",
        re.I,
    )
    starts = list(col_re.finditer(section))
    if not starts:
        return {}
    out: dict[str, str] = {}
    for i, sm in enumerate(starts):
        field = sm.group(1)
        rest_end = starts[i + 1].start() if i + 1 < len(starts) else len(section)
        desc = section[sm.end() : rest_end].strip()
        desc = re.sub(
            r"\s*ESM-1v Predictions Documentation(?:\.md)?\s+"
            r"\d{4}-\d{2}-\d{2}\s+\d+\s*/\s*\d+\s*",
            " ",
            desc,
            flags=re.I,
        ).strip()
        if field and desc:
            out[field] = desc
    return out


def parse_fields_bullet_name_type_equals_description(text: str) -> dict[str, str]:
    """
    VAMP-seq-style ``Fields`` section: bullet ``{field_name}: {type} = {description}``.
    Sub-bullets (○) are appended to the preceding field description.
    """
    text = _normalize_pdf_ligatures(text)
    m = re.search(r"\bFields\b\s*(.*)", text, re.I | re.DOTALL)
    if not m:
        return {}
    section = re.sub(r"\s+", " ", m.group(1)).strip()
    main_re = re.compile(
        r"[●*]\s*"
        r"([a-zA-Z][a-zA-Z0-9_<>\{\}]*):\s*"
        r"(\w+)\s*=\s*"
        r"(.*?)"
        r"(?=\s*[●*]\s*[a-zA-Z][a-zA-Z0-9_<>\{\}]*:\s*\w+\s*=|$)",
        re.DOTALL,
    )
    out: dict[str, str] = {}
    for sm in main_re.finditer(section):
        field = sm.group(1).strip()
        desc = sm.group(3).strip()
        if "○" in desc:
            base, *subs = desc.split("○")
            parts = [base.strip(), *[s.strip() for s in subs if s.strip()]]
            desc = ". ".join(parts).strip()
        if field and desc:
            out[field] = desc
    return out


def parse_type_column_name_description_table(text: str) -> dict[str, str]:
    """
    Three-column tables: ``Type``, ``Column Name``, ``Description`` (variant effects
    on gene expression and similar). The type column (string, uint, float) is ignored.
    """
    text = _normalize_pdf_ligatures(text)
    if not re.search(r"Type\s+Column\s+Name\s+Description", text, re.I):
        return {}
    m = re.search(
        r"Type\s+Column\s+Name\s+Description\s*(.*)",
        text,
        re.I | re.DOTALL,
    )
    if not m:
        return {}
    section = re.sub(r"\s+", " ", m.group(1)).strip()
    row_re = re.compile(
        r"\b(string|uint|float)\s+"
        r"([A-Za-z][a-zA-Z0-9_]*)\s+"
        r"(?:Required\.|Optional\.)\s+"
        r"(.*?)"
        r"(?=\s+(?:string|uint|float)\s+[A-Za-z]|$)",
        re.DOTALL,
    )
    out: dict[str, str] = {}
    for sm in row_re.finditer(section):
        field = sm.group(2)
        desc = sm.group(3).strip()
        if field and desc:
            out[field] = desc
    return out


def parse_column_name_description_table(text: str) -> dict[str, str]:
    """
    Two-column tables: ``Column name`` and ``Description`` only (MutPred2 property
    scores and similar). Distinct from the four-column SEMpl/TLand layout.
    """
    text = _normalize_pdf_ligatures(text)
    if re.search(
        r"Column\s+name\s+Data\s*type\s+Example\s+Description",
        text,
        re.I,
    ):
        return {}
    m = re.search(
        r"Column\s+name\s+Description\s*(.*?)(?:List\s+of\s+Properties|\Z)",
        text,
        re.I | re.DOTALL,
    )
    if not m:
        return {}
    section = re.sub(r"\s+", " ", m.group(1)).strip()
    row_re = re.compile(
        r"\b(MutPred2 score|Substitution|Mechanisms|[a-z][a-z0-9_]+)\s+"
        r"(?=The |Gives |HGNC |A JSON)",
    )
    starts = list(row_re.finditer(section))
    out: dict[str, str] = {}
    for i, sm in enumerate(starts):
        field = sm.group(1).strip()
        if field.lower() in ("column", "name", "description"):
            continue
        rest_end = starts[i + 1].start() if i + 1 < len(starts) else len(section)
        desc = section[sm.end() : rest_end].strip()
        if field and desc:
            out[field] = desc
    return out


def parse_columns_name_type_example_description(text: str) -> dict[str, str]:
    """
    ``Columns`` tables with header row ``Column name | Data type | Example | Description``
    (SEMpl / TLand prediction files and similar). PDF text is flattened; each data row
    starts with ``<field> <type> <example> <description>``.
    """
    text = _normalize_pdf_ligatures(text)
    m = re.search(
        r"\bColumns\s+Column\s+name\s+Data\s*type\s+Example\s+Description\s*(.*)",
        text,
        re.I | re.DOTALL,
    )
    if not m:
        return {}
    section = m.group(1)
    row_re = re.compile(
        r"(\{[a-zA-Z_]+\}\.[A-Za-z][\w]*|[A-Za-z][\w.]*)\s+"
        r"(str|int|float|Float)\s+",
        re.IGNORECASE,
    )
    starts = list(row_re.finditer(section))
    out: dict[str, str] = {}
    skip_names = frozenset({"column", "data", "example", "description"})
    for i, sm in enumerate(starts):
        field = sm.group(1)
        if field.lower() in skip_names:
            continue
        rest_end = starts[i + 1].start() if i + 1 < len(starts) else len(section)
        rest = section[sm.end() : rest_end]
        desc = re.sub(r"\s+", " ", _split_type_example_description(rest)).strip()
        if field and desc:
            out[field] = desc
    return out


def parse_numbered_field_colon_description(text: str) -> dict[str, str]:
    """
    Numbered lists ``1. {field_name}: {description}`` (BlueSTARR file format specs).
    """
    text = _normalize_pdf_ligatures(text)
    flat = re.sub(r"\s+", " ", text).strip()
    if not re.search(r"\d+\.\s+[^:]+:\s+", flat):
        return {}
    row_re = re.compile(
        r"\d+\.\s+"
        r"([^:]+?):\s*"
        r"(.*?)"
        r"(?=\s+\d+\.\s+[^:]+:|$)",
    )
    out: dict[str, str] = {}
    for sm in row_re.finditer(flat):
        field = sm.group(1).strip()
        desc = sm.group(2).strip()
        if field and desc:
            out[field] = desc
    return out if len(out) >= 2 else {}


def parse_numbered_columns_section(text: str) -> dict[str, str]:
    """
    ``Columns`` sections with numbered rows ``1. field* - description`` (IGVF MPRA
    metadata and similar). PDF text often omits spaces; descriptions are taken from
    text after ``-`` until the next sequential column number.
    """
    col = re.search(r"Columns\s*\(.*?\)\s*:(.*)", text, re.I | re.DOTALL)
    if not col:
        return {}
    section = re.split(r"\bNote:Forstrings", col.group(1), maxsplit=1)[0]

    headers = list(re.finditer(r"(\d+)\.\s*([A-Za-z_]+)\*?\s*-", section))
    chain: list[re.Match[str]] = []
    for hm in headers:
        num = int(hm.group(1))
        name = hm.group(2)
        if name == "SPDI" and num >= 100:
            num = 13
        if not chain and num == 1:
            chain.append(hm)
        elif chain and num == len(chain) + 1:
            chain.append(hm)

    out: dict[str, str] = {}
    for i, hm in enumerate(chain):
        desc_end = chain[i + 1].start() if i + 1 < len(chain) else len(section)
        desc = section[hm.end() : desc_end]
        desc = re.split(r"Note:", desc, maxsplit=1)[0]
        desc = re.split(r"https?://", desc, maxsplit=1)[0]
        desc = re.split(r"(?<=[a-z])(?=\d+\.\s*[A-Za-z_])", desc)[0]
        desc = re.sub(r"\s+", " ", desc).strip()
        field = hm.group(2)
        if field.lower() == "spdi":
            field = "SPDI"
        if field and desc:
            out[field] = desc
    return out


def parse_yaml_colon_type_description(text: str) -> dict[str, str]:
    """
    Blocks like ``field_name:`` followed by ``\\t<type>, <description>`` (DUAL-IPA style).
    """
    out: dict[str, str] = {}
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z_][\w]*)\s*:\s*$", lines[i].strip())
        if not m:
            i += 1
            continue
        key = m.group(1)
        i += 1
        if i >= len(lines):
            break
        body = lines[i].strip()
        if body:
            # strip leading type token (e.g. "character, ..." or "float, ...")
            parts = body.split(",", 1)
            desc = parts[1].strip() if len(parts) == 2 else body
            if desc:
                out[key] = desc
        i += 1
    return out


def parse_markdown_bullet_fields(text: str) -> dict[str, str]:
    """Lines like ``* field_name: description`` (SGE score spec style)."""
    out: dict[str, str] = {}
    for ln in text.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^\s*\*\s*([A-Za-z_][\w]*)\s*:\s*(.+)$", ln)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def parse_tsv_field_description_lines(text: str) -> dict[str, str]:
    """``field<TAB>type, prose`` lines (TF_impactscore style)."""
    out: dict[str, str] = {}
    for ln in text.replace("\r\n", "\n").split("\n"):
        if "\t" not in ln:
            continue
        k, v = ln.split("\t", 1)
        k = k.strip()
        v = v.strip()
        if not k or not v:
            continue
        if not re.match(r"^[A-Za-z_][\w]*$", k):
            continue
        out[k] = v
    return out


def parse_file_format_specification_text(text: str) -> dict[str, str]:
    """
    Merge outputs from several heuristics (first parser to emit a key wins).
    Parsers are ordered from most structured (AutoSQL) to loosest (TSV lines).

    When a document-specific parser fully matches (ESM-1v columns, VAMP-seq Fields,
    MutPred2 two-column table), only that parser's output is used.
    """
    for fn in (
        parse_columns_are_as_follows_colon_descriptions,
        parse_fields_bullet_name_type_equals_description,
        parse_type_column_name_description_table,
        parse_column_name_description_table,
        parse_numbered_field_colon_description,
    ):
        fields = fn(text)
        if fields:
            return dict(sorted(fields.items(), key=lambda kv: kv[0].lower()))
    parsers: list[Callable[[str], dict[str, str]]] = [
        parse_autosql,
        parse_columns_name_type_example_description,
        parse_numbered_columns_section,
        parse_name_type_description_table,
        parse_column_header_table,
        parse_html_table,
        parse_pipe_column_lines,
        parse_yaml_colon_type_description,
        parse_markdown_bullet_fields,
        parse_space_dash,
        parse_tab_kv_body,
        parse_tsv_field_description_lines,
    ]
    merged: dict[str, str] = {}
    for fn in parsers:
        for k, v in fn(text).items():
            if not k or not v or k in merged:
                continue
            merged[k] = v
    return merged


def extract_text_from_attachment(data: bytes, filename: str) -> str | None:
    """Return UTF-8-ish text for parsing, or None if unsupported."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        txt = _pdf_to_text(data)
        return txt
    if lower.endswith((".txt", ".tsv", ".csv", ".md", ".as", ".json")):
        for enc in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", errors="replace")
    if lower.endswith(".html") or lower.endswith(".htm"):
        raw = data.decode("utf-8", errors="replace")
        raw = re.sub(r"(?is)<script[^>]*>.*?</script>", "", raw)
        raw = re.sub(r"(?is)<style[^>]*>.*?</style>", "", raw)
        return raw
    return None


def _pdf_to_text(data: bytes) -> str | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(io.BytesIO(data))
        parts: list[str] = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        return "\n".join(parts) if parts else None
    except Exception:
        return None
