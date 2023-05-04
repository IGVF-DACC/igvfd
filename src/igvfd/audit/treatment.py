from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Treatment', frame='object')
def audit_treatment_term_id_check(value, system):
    '''If treatment_term_id starts with NTR, flag treatment object with warning audit.'''
    if 'treatment_term_id' in value:
        treatment_id = value['@id']
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            detail = f'Treatment {audit_link(path_to_text(treatment_id, treatment_id))} has term_id {audit_link(term_id,term_id)}.'
            yield AuditFailure('treatment_term_id starts with NTR', detail, level='WARNING')
