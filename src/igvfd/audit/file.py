from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description,
    space_in_words
)


@audit_checker('File', frame='object')
def audit_upload_status(value, system):
    '''
    [
        {
            "audit_description": "Files are expected to be validated.",
            "audit_category": "upload status not validated",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "External files are expected to be validated.",
            "audit_category": "upload status not validated",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    upload_status = value.get('upload_status')
    if upload_status not in ['validated']:
        if value.get('external'):
            audit_level = 'WARNING'
            description = get_audit_description(audit_upload_status, index=1)
        else:
            audit_level = 'ERROR'
            description = get_audit_description(audit_upload_status, index=0)
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `upload_status` {upload_status}.'
        )
        if upload_status == 'invalidated':
            validation_error_detail = value.get('validation_error_detail')
            detail = f'{detail} Validation error detail: {validation_error_detail}'
        yield AuditFailure(
            'upload status not validated',
            f'{detail} {description}',
            level=audit_level
        )
