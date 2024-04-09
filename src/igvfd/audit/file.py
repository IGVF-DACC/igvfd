from snovault.auditor import (
    audit_checker,
    AuditFailure,
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
    detail = (
        f'Move controlled-access file {value["@id"]} '
        f'from submission AnVIL workspace to protected AnVIL workspace. '
        f'Source={value["anvil_source_url"]} '
        f'Destination={value["anvil_destination_url"]}'
    )
    yield AuditFailure(
        'incorrect anvil workspace',
        detail,
        level='INTERNAL_ACTION'
    )
