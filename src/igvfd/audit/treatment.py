from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('Treatment', frame='object')
def audit_treatment_term_id_check(value, system):
    '''
    [
        {
            "audit_description": "Treatments with a newly requested term ID are expected to have it updated following its addition to the appropriate ontology database.",
            "audit_category": "NTR term ID",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    description = get_audit_description(audit_treatment_term_id_check)
    if 'treatment_term_id' in value:
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            treatment_id = value['@id']
            detail = f'Treatment term for {audit_link(path_to_text(treatment_id), treatment_id)} has been newly requested.'
            yield AuditFailure('NTR term ID', f'{detail} {description}', level='INTERNAL_ACTION')
