from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


@audit_checker('TabularFile', frame='object')
def audit_tabular_file_no_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "Tabular files are expected to link to a file format specifications document describing the headers of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_tabular_file_no_file_format_specifications, index=0)
    if not (value.get('file_format_specifications')):
        detail = (
            f'Tabular file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `file_format_specifications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
