from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Tissue', frame='object')
def audit_tissue_ccf_id(value, system):
    '''
    [
        {
            "audit_description": "Human tissues are expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "missing CCF ID",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    if ('ccf_id' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'is missing common coordinate framework identifier (CCF ID).'
        )
        yield AuditFailure('missing CCF ID', detail, level='NOT_COMPLIANT')


@audit_checker('Tissue', frame='object')
def audit_tissue_ccf_id_nonhuman_sample(value, system):
    '''
    [
        {
            "audit_description": "Non-human tissues are not expected to specify a common coordinate framework identifier (CCF ID).",
            "audit_category": "unexpected CCF ID",
            "audit_level": "ERROR"
        }
    ]
    '''
    if ('ccf_id' in value) and (value.get('taxa', '') != 'Homo sapiens'):
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'has common coordinate framework identifier (CCF ID) '
            f'but is associated with a non-human donor.'
        )
        yield AuditFailure('unexpected CCF ID', detail, level='ERROR')
