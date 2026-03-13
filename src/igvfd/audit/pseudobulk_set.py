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
            "audit_description": "The source biosamples of pseudobulk sets should be one of the samples associated with the input file sets.",
            "audit_category": "inconsistent samples",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_sample_matches_input, index=0)
    input_file_set_samples = []
    if value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object_with_select_calculated_properties?field=samples')
            input_file_set_samples.extend([x for x in input_file_set_object.get('samples', [])])
    if value.get('samples', []):
        mismatched_samples = []
        for sample in value.get('samples', []):
            if sample not in input_file_set_samples:
                mismatched_samples.append(sample)
        if mismatched_samples:
            detail = (
                f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has source biosample(s) {", ".join([audit_link(path_to_text(sample_id), sample_id) for sample_id in mismatched_samples])} '
                f'not associated with any of the input file sets.'
            )
            yield AuditFailure(
                audit_message.get('audit_category', ''),
                f'{detail} {audit_message.get("audit_description", "")}',
                level=audit_message.get('audit_level', '')
            )


def audit_pseudobulk_set_input_file_set_type(value, system):
    '''
    [
        {
            "audit_description": "The input curated sets of pseudobulk sets should have the `file_set_type` external sequencing data.",
            "audit_category": "unexpected input file sets",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_input_file_set_type, index=0)
    if value.get('input_file_sets', []):
        for input_file_set in value.get('input_file_sets', []):
            input_file_set_object = system.get('request').embed(
                input_file_set, '@@object?skip_calculated=true')
            if input_file_set_object['@type'][0] == 'CuratedSet':
                if input_file_set_object.get('file_set_type') != 'external sequencing data':
                    detail = (
                        f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'has curated set {audit_link(path_to_text(input_file_set), input_file_set)} in input file sets '
                        f'but the file_set_type is "{input_file_set_object.get("file_set_type", "")}".'
                    )
                    yield AuditFailure(
                        audit_message.get('audit_category', ''),
                        f'{detail} {audit_message.get("audit_description", "")}',
                        level=audit_message.get('audit_level', '')
                    )


function_dispatcher_pseudobulk_set_object = {
    'audit_pseudobulk_set_marker_gene_files': audit_pseudobulk_set_marker_gene_files,
    'audit_pseudobulk_set_sample_matches_input': audit_pseudobulk_set_sample_matches_input,
    'audit_pseudobulk_set_input_file_set_type': audit_pseudobulk_set_input_file_set_type
}


@audit_checker('PseudobulkSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_pseudobulk_set_object.values()))
def audit_pseudobulk_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_pseudobulk_set_object.keys():
        for failure in function_dispatcher_pseudobulk_set_object[function_name](value, system):
            yield failure
