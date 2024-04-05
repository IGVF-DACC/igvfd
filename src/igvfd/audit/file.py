from snovault.auditor import (
    audit_checker,
    AuditFailure,
)


@audit_checker('File', frame='object')
def audit_file_controlled_access_file_in_correct_anvil_workspace(value, system):
    if value.get('controlled_access', False) is False:
        return
    if value.get('upload_status') != 'pending':
        return
    detail = (
        f'Move controlled-access file {value["@id"]} '
        f'from submission Anvil workspace to protected Anvil workspace. '
        f'Source={value["anvil_source_url"]} '
        f'Destination={value["anvil_destination_url"]}'
    )
    yield AuditFailure(
        'incorrect anvil workspace',
        detail,
        level='INTERNAL_ACTION'
    )
