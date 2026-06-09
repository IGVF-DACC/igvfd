from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def audit_pseudobulk_set_marker_gene_files(value, system):
    '''
    [
        {
            "audit_description": "Pseudobulk sets require a marker genes file in their input file set(s).",
            "audit_category": "missing marker gene list",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_marker_gene_files, index=0)
    marker_genes_files_in_input_file_set = []
    if value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object_with_select_calculated_properties?field=files')
            files_in_input = input_file_set_object.get('files', [])
            for tab_file in [x for x in files_in_input if x.startswith('/tabular-files/')]:
                file_object = system.get('request').embed(tab_file, '@@object?skip_calculated=true')
                if file_object.get('content_type', '') == 'marker genes':
                    marker_genes_files_in_input_file_set.append(file_object.get('@id'))
    if not marker_genes_files_in_input_file_set:
        detail = (
            f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no input file sets that have marker genes files.'
        )
        yield AuditFailure(
            audit_message.get('audit_category', ''),
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_message.get('audit_level', '')
        )


def audit_pseudobulk_set_sample_matches_input(value, system):
    '''
    [
        {
            "audit_description": "The parent samples of pseudobulk sets should be one of the samples associated with the input file sets.",
            "audit_category": "inconsistent samples",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "The parent samples of merged pseudobulk sets should be all of the samples associated with the input file sets.",
            "audit_category": "inconsistent samples",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_non_merged = get_audit_message(audit_pseudobulk_set_sample_matches_input, index=0)
    audit_message_merged = get_audit_message(audit_pseudobulk_set_sample_matches_input, index=1)
    input_file_set_samples = []
    if value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object_with_select_calculated_properties?field=samples')
            input_file_set_samples.extend([x for x in input_file_set_object.get('samples', [])])
    if value.get('merged', False):
        if value.get('samples', []):
            if set(value.get('samples', [])) != set(input_file_set_samples):
                merged_pseudobulk_parent_sample_links = ', '.join(
                    [
                        audit_link(path_to_text(sample_id), sample_id) for
                        sample_id in sorted(list(set(value.get('samples', []))))
                    ]
                )
                input_sample_links = ', '.join(
                    [
                        audit_link(path_to_text(sample_id), sample_id) for
                        sample_id in sorted(input_file_set_samples)
                    ]
                )
                detail = (
                    f'Merged pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has a set of parent sample(s) {merged_pseudobulk_parent_sample_links} which '
                    f'do not match the samples of the input file sets: {input_sample_links}.'
                )
                yield AuditFailure(
                    audit_message_merged.get('audit_category', ''),
                    f'{detail} {audit_message_merged.get("audit_description", "")}',
                    level=audit_message_merged.get('audit_level', '')
                )
    else:
        if value.get('samples', []):
            mismatched_samples = []
            for sample in value.get('samples', []):
                if sample not in input_file_set_samples:
                    mismatched_samples.append(sample)
            if mismatched_samples:
                input_sample_links = ', '.join(
                    [audit_link(path_to_text(sample_id), sample_id) for sample_id in mismatched_samples]
                )
                detail = (
                    f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has parent sample(s) {input_sample_links} not associated with any of the input file sets.'
                )
                yield AuditFailure(
                    audit_message_non_merged.get('audit_category', ''),
                    f'{detail} {audit_message_non_merged.get("audit_description", "")}',
                    level=audit_message_non_merged.get('audit_level', '')
                )


def audit_pseudobulk_set_input_file_set_type(value, system):
    '''
    [
        {
            "audit_description": "Pseudobulk sets are expected to have input curated sets with `file_set_type` of `external sequencing data` only.",
            "audit_category": "unexpected input file set type",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_input_file_set_type, index=0)
    if value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object_with_select_calculated_properties?field=@type')
            if input_file_set_object['@type'][0] == 'CuratedSet':
                if input_file_set_object.get('file_set_type') != 'external sequencing data':
                    detail = (
                        f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'has curated set {audit_link(path_to_text(input_file_set), input_file_set)} in input file sets '
                        f'but the `file_set_type` is "{input_file_set_object.get("file_set_type", "")}".'
                    )
                    yield AuditFailure(
                        audit_message.get('audit_category', ''),
                        f'{detail} {audit_message.get("audit_description", "")}',
                        level=audit_message.get('audit_level', '')
                    )


def audit_pseudobulk_set_parent_samples_mixed_classifications_terms(value, system):
    '''
    [
        {
            "audit_description": "The parent samples of pseudobulk sets are expected to all share the same biosample classifications.",
            "audit_category": "inconsistent parent samples",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "The parent samples of pseudobulk sets are expected to all share the same sample terms.",
            "audit_category": "inconsistent parent samples",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message_classifications = get_audit_message(
        audit_pseudobulk_set_parent_samples_mixed_classifications_terms, index=0)
    audit_message_terms = get_audit_message(audit_pseudobulk_set_parent_samples_mixed_classifications_terms, index=1)
    classifications = set()
    terms = set()
    if value.get('samples', []):
        for sample in value.get('samples', []):
            parent_sample_object = system.get('request').embed(
                sample, '@@object_with_select_calculated_properties?field=classifications')
            classifications.add(', '.join(
                sorted(parent_sample_object.get('classifications', []))
            ))
            terms.add(', '.join(
                sorted(parent_sample_object.get('sample_terms', []))
            ))
    if len(classifications) > 1:
        detail = (
            f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has parent samples with different sets of classifications: '
            f'{"; ".join(classifications)}.'
        )
        yield AuditFailure(
            audit_message_classifications.get('audit_category', ''),
            f'{detail} {audit_message_classifications.get("audit_description", "")}',
            level=audit_message_classifications.get('audit_level', '')
        )
    if len(terms) > 1:
        term_links = []
        for term in sorted(list(terms)):
            term_links.append(', '.join([audit_link(path_to_text(x), x) for x in term.split(', ')]))
        detail = (
            f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has parent samples with different sets of sample terms: '
            f'{"; ".join(term_links)}.'
        )
        yield AuditFailure(
            audit_message_terms.get('audit_category', ''),
            f'{detail} {audit_message_terms.get("audit_description", "")}',
            level=audit_message_terms.get('audit_level', '')
        )


def audit_pseudobulk_set_mismatched_merged_cell_types(value, system):
    '''
    [
        {
            "audit_description": "The inputs to merged pseudobulk sets are expected to have the same cell type as the merged pseudobulk set.",
            "audit_category": "mismatched merged cell types",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_mismatched_merged_cell_types, index=0)
    current_cell_type = value.get('cell_type', '')
    cell_types = set()
    if value.get('merged', False) and value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object?skip_calculated=true')
            cell_types.add(input_file_set_object.get('cell_type', ''))
    if any([x != current_cell_type for x in sorted(list(cell_types))]):
        cell_type_links = ', '.join([audit_link(path_to_text(x), x) for x in sorted(list(cell_types))])
        detail = (
            f'Merged pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has the cell type {current_cell_type}, but its input pseudobulk sets have '
            f'mismatched cell types: {cell_type_links}.'
        )
        yield AuditFailure(
            audit_message.get('audit_category', ''),
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_message.get('audit_level', '')
        )


function_dispatcher_pseudobulk_set_object = {
    'audit_pseudobulk_set_marker_gene_files': audit_pseudobulk_set_marker_gene_files,
    'audit_pseudobulk_set_sample_matches_input': audit_pseudobulk_set_sample_matches_input,
    'audit_pseudobulk_set_input_file_set_type': audit_pseudobulk_set_input_file_set_type,
    'audit_pseudobulk_set_parent_samples_mixed_classifications_terms': audit_pseudobulk_set_parent_samples_mixed_classifications_terms,
    'audit_pseudobulk_set_mismatched_merged_cell_types': audit_pseudobulk_set_mismatched_merged_cell_types
}


@audit_checker('PseudobulkSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_pseudobulk_set_object.values()))
def audit_pseudobulk_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_pseudobulk_set_object.keys():
        for failure in function_dispatcher_pseudobulk_set_object[function_name](value, system):
            yield failure
