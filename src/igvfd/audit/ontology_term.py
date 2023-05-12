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
    OntologyTerm objects with a `term_id` that starts with NTR should be flagged with a warning audit.
    '''
    if 'term_id' in value:
        ontologyterm_id = value['@id']
        term_id = value['term_id']
        if term_id.startswith('NTR'):
            detail = f'Ontology term for {audit_link(ontologyterm_id, ontologyterm_id)} has been newly requested. Term {audit_link(term_id,term_id)} will be replaced with another term_id following its addition to the appropriate ontology database.'
            yield AuditFailure('Ontology term has been newly requested', detail, level='WARNING')
