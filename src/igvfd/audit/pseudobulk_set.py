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
            "audit_description": "Pseudobulk sets should link to the marker gene list relevant for the annotated cells.",
            "audit_category": "missing marker gene list",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_pseudobulk_set_marker_gene_files, index=0)
    marker_gene_file = value.get('marker_gene_file', '')
    if marker_gene_file:
        file = system.get('request').embed(marker_gene_file, '@@object?skip_calculated=true')
        if file.get('content_type', '') != 'marker genes':
            detail = (
                f'Pseudobulk set {audit_link(path_to_text(value["@id"]), value["@id"])} has no '
                f'linked files in `marker_gene_file` with `content_type` marker genes.'
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
