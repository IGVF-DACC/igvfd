from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('OntologyTerm', frame='object')
def audit_ntr_term_id(value, system):
    '''
    [
        {
            "audit_description": "Ontology terms with a newly requested term ID are expected to have it updated following its addition to the appropriate ontology database.",
            "audit_category": "NTR term id",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    description = get_audit_description(audit_ntr_term_id)
    if 'term_id' in value:
        ontologyterm_id = value['@id']
        term_id = value['term_id']
        if term_id.startswith('NTR'):
            detail = f'Ontology term for {audit_link(ontologyterm_id, ontologyterm_id)} has been newly requested. Term {audit_link(term_id,term_id)} should be replaced with another `term_id` following its addition to the appropriate ontology database.'
            yield AuditFailure('NTR term ID', f'{detail} {description}', level='INTERNAL_ACTION')
