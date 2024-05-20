from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('File', frame='object')
def audit_file_controlled_access_file_in_correct_anvil_workspace(value, system):
    '''
    [
        {
            "audit_description": "All controlled access files have to be moved from lab submission AnVIL workspace to DACC AnVIL workspace.",
            "audit_category": "incorrect anvil workspace",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    if value.get('controlled_access', False) is False:
        return
    if value.get('upload_status') != 'pending':
        return
    description = get_audit_description(audit_file_controlled_access_file_in_correct_anvil_workspace)
    detail = (
        f'Move controlled access file {audit_link(path_to_text(value["@id"]), value["@id"])} '
        f'from submission AnVIL workspace to protected AnVIL workspace. '
        f'Source={value["anvil_source_url"]} '
        f'Destination={value["anvil_destination_url"]}'
    )
    yield AuditFailure(
        'incorrect anvil workspace',
        f'{detail} {description}',
        level='INTERNAL_ACTION'
    )


@audit_checker('File', frame='object')
def audit_upload_status(value, system):
    '''
    [
        {
            "audit_description": "Files are expected to be validated.",
            "audit_category": "invalid upload status",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_upload_status)
    upload_status = value.get('upload_status')
    if upload_status not in ['validated', 'deposited']:
        if value.get('external'):
            audit_level = 'WARNING'
        else:
            audit_level = 'ERROR'
        detail = (
            f'File {audit_link(path_to_text(value["@id"]), value["@id"])} has `upload_status` {upload_status}.'
        )
        yield AuditFailure(
            'invalid upload status',
            f'{detail} {description}',
            level=audit_level
        )
