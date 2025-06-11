from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


def audit_external_reference_files(value, system):
    '''
    [
        {
            "audit_description": "Reference files uploaded from external resources are expected to have external identifiers in dbxrefs.",
            "audit_category": "missing dbxrefs",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_external_reference_files)
    object_type = space_in_words(value['@type'][0]).capitalize()
    if value.get('external'):
        if 'dbxrefs' not in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} is an external file, '
                f'but does not have identifier(s) from an external resource listed in `dbxrefs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_reference_file_object = {
    'audit_external_reference_files': audit_external_reference_files
}


@audit_checker('ReferenceFile', frame='object')
def audit_reference_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_reference_file_object.keys():
        for failure in function_dispatcher_reference_file_object[function_name](value, system):
            yield failure
