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
        audit_detail: This treatment term has been newly requested. It will be replaced with a CHEBI or UNIPROT term following its addition to the appropriate ontology database.
        audit_category: treatment term has been newly requested
        audit_level: INTERNAL_ACTION
    '''
    if 'treatment_term_id' in value:
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            treatment_id = value['@id']
            detail = f'Treatment term for {audit_link(treatment_id, treatment_id)} has been newly requested. Term {audit_link(term_id,term_id)} will be replaced with a CHEBI or UNIPROT term following its addition to the appropriate ontology database.'
            yield AuditFailure('treatment term has been newly requested', detail, level='INTERNAL_ACTION')
