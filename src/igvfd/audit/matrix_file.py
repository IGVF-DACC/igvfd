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


def audit_matrix_file_dimensions(value, system):
    '''
    [
        {
            "audit_description": "Matrix files, with the exception of .hic, .cool, and .mcool files, are expected to have different values for each dimension.",
            "audit_category": "inconsistent dimensions",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_matrix_file_dimensions)
    if value['file_format'] not in ['hic', 'cool', 'mcool'] and value['principal_dimension'] in value['secondary_dimensions']:
        detail = (
            f'Matrix file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has {value["principal_dimension"]} for both `principal_dimension` and `secondary_dimensions`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_matrix_file_object = {
    'audit_matrix_file_dimensions': audit_matrix_file_dimensions
}


@audit_checker('MatrixFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_matrix_file_object.values()))
def audit_matrix_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_matrix_file_object.keys():
        for failure in function_dispatcher_matrix_file_object[function_name](value, system):
            yield failure
