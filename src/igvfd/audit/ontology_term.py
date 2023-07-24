from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('OntologyTerm', frame='object')
def audit_ntr_term_id(value, system):
    '''
        audit_detail: Ontology terms with a newly requested term ID should have it updated following its addition to the appropriate ontology database.
        audit_category: Ontology term has been newly requested
        audit_levels: INTERNAL_ACTION
    '''
    if 'term_id' in value:
        ontologyterm_id = value['@id']
        term_id = value['term_id']
        if term_id.startswith('NTR'):
            detail = f'Ontology term for {audit_link(ontologyterm_id, ontologyterm_id)} has been newly requested. Term {audit_link(term_id,term_id)} will be replaced with another term_id following its addition to the appropriate ontology database.'
            yield AuditFailure('Ontology term has been newly requested', detail, level='INTERNAL_ACTION')
