from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def audit_tissue_ccf_id(value, system):
    '''
    [
        {
            "audit_description": "Human tissues/organs are expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "missing CCF ID",
            "audit_level": "INTERNAL_ACTION"
        },
        {
            "audit_description": "Non-human tissues/organs are not expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "unexpected CCF ID",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    audit_message_human_tissue = get_audit_message(audit_tissue_ccf_id, index=0)
    audit_message_non_human_tissue = get_audit_message(audit_tissue_ccf_id, index=1)
    if ('ccf_id' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        value_id = system.get('path')
        detail = (
            f'Tissue/Organ {audit_link(path_to_text(value_id), value_id)} '
            f'is missing a `ccf_id`.'
        )
        yield AuditFailure(audit_message_human_tissue.get('audit_category', ''), f'{detail} {audit_message_human_tissue.get("audit_description", "")}', level=audit_message_human_tissue.get('audit_level', ''))
    if ('ccf_id' in value) and (value.get('taxa', '') != 'Homo sapiens'):
        value_id = system.get('path')
        detail = (
            f'Tissue/Organ {audit_link(path_to_text(value_id), value_id)} '
            f'has a `ccf_id` but is associated with a non-human donor.'
        )
        yield AuditFailure(audit_message_non_human_tissue.get('audit_category', ''), f'{detail} {audit_message_non_human_tissue.get("audit_description", "")}', level=audit_message_non_human_tissue.get('audit_level', ''))


function_dispatcher_tissue_object = {
    'audit_tissue_ccf_id': audit_tissue_ccf_id
}


@audit_checker('Tissue', frame='object')
def audit_tissue_object_dispatcher(value, system):
    for function_name in function_dispatcher_tissue_object.keys():
        for failure in function_dispatcher_tissue_object[function_name](value, system):
            yield failure
