from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description,
    space_in_words
)


@audit_checker('OntologyTerm', frame='object')
def audit_ntr_term_id(value, system):
    '''
    [
        {
            "audit_description": "Ontology terms with a newly requested term ID are expected to have it updated following its addition to the appropriate ontology database.",
            "audit_category": "NTR term ID",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    description = get_audit_description(audit_ntr_term_id)
    if 'term_id' in value:
        ontologyterm_id = value['@id']
        term_id = value['term_id']
        if term_id.startswith('NTR'):
            detail = f'{object_type} for {audit_link(path_to_text(ontologyterm_id), ontologyterm_id)} has been newly requested.'
            yield AuditFailure('NTR term ID', f'{detail} {description}', level='INTERNAL_ACTION')
