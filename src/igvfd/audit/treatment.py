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
    '''This treatment term has been newly requested. It will be replaced with an UNIPROT or CHEBI term following it's addition to the appropriate ontology database.'''
    if 'treatment_term_id' in value:
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            treatment_id = value['@id']
            detail = f'Treatment {audit_link(treatment_id, treatment_id)} has term_id {audit_link(term_id,term_id)}.'
            yield AuditFailure('treatment term has been newly requested', detail, level='WARNING')
