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
    '''
    [
        {
            "audit_description": "Treatments with a newly requested term ID are expected to have it updated following its addition to the appropriate ontology database.",
            "audit_category": "NTR treatment term id",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    if 'treatment_term_id' in value:
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            treatment_id = value['@id']
            detail = f'Treatment term for {audit_link(treatment_id, treatment_id)} has been newly requested. Term {audit_link(term_id,term_id)} will be replaced with a CHEBI or UNIPROT term following its addition to the appropriate ontology database.'
            yield AuditFailure('NTR treatment term ID', detail, level='INTERNAL_ACTION')
