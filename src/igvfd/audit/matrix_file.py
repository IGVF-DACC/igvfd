from snovault.auditor import (
    AuditFailure
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, register_all_audits


@register_audit(['MatrixFile'], frame='object')
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


register_all_audits()
