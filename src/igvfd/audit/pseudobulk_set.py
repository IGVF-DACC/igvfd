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


def audit_pseudobulk_set_marker_gene_files(value, system, input_file_sets=None):
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
    if input_file_sets:
        for input_file_set in input_file_sets:
            input_file_set_object = system.get('request').embed(input_file_set, '@@object?skip_calculated=true')
            files_in_input = input_file_set_object.get('files', [])
            for tab_file in [x for x in files_in_input if x.startswith('/tabular-file/')]:
                file_object = system.get('request').embed(tab_file, '@@object?skip_calculated=true')
                if file_object.get('content_type', '') == 'marker genes':
                    marker_genes_files_in_input_file_set.append(file_object['@id'])
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


function_dispatcher_pseudobulk_set_object = {
    'audit_pseudobulk_set_marker_gene_files': audit_pseudobulk_set_marker_gene_files
}


@audit_checker('PseudobulkSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_pseudobulk_set_object.values()))
def audit_pseudobulk_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_pseudobulk_set_object.keys():
        for failure in function_dispatcher_pseudobulk_set_object[function_name](value, system):
            yield failure
