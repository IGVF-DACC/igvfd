from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('Tissue', frame='object')
def audit_tissue_ccf_id(value, system):
    '''
    [
        {
            "audit_description": "Human tissues are expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "missing CCF ID",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Non-human tissues are not expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "unexpected CCF ID",
            "audit_level": "ERROR"
        }
    ]
    '''
    description_human_tissue = get_audit_description(audit_tissue_ccf_id, index=0)
    description_non_human_tissue = get_audit_description(audit_tissue_ccf_id, index=1)
    if ('ccf_id' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'is missing a `ccf_id`.'
        )
        yield AuditFailure('missing CCF ID', f'{detail} {description_human_tissue}', level='NOT_COMPLIANT')
    if ('ccf_id' in value) and (value.get('taxa', '') != 'Homo sapiens'):
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'has a `ccf_id` but is associated with a non-human donor.'
        )
        yield AuditFailure('unexpected CCF ID', f'{detail} {description_non_human_tissue}', level='ERROR')
