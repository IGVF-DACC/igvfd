from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, run_audits


@register_audit(['ModelSet'], frame='object')
def audit_external_input_data_content_type(value, system):
    '''
    [
        {
            "audit_description": "Tabular files linked as `external_input_data` must be of type external source data.",
            "audit_category": "inconsistent external input data",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_inconsistent_external_input_data = get_audit_message(audit_external_input_data_content_type, index=0)
    detail = ''
    if 'external_input_data' in value:
        external_input_data = value.get('external_input_data', '')
        external_input_data_object = system.get('request').embed(external_input_data, '@@object?skip_calculated=true')
        if external_input_data_object['content_type'] != 'external source data':
            detail = (
                f'The `content_type` of `external_input_data` file '
                f'{audit_link(path_to_text(external_input_data), external_input_data)} '
                f'is {external_input_data_object["content_type"]}.'
            )
            yield AuditFailure(
                audit_message_inconsistent_external_input_data.get('audit_category', ''),
                f'{detail} {audit_message_inconsistent_external_input_data.get("audit_description", "")}',
                level=audit_message_inconsistent_external_input_data.get('audit_level', '')
            )


@audit_checker('ModelSet', frame='object')
def audit_model_set_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')
