from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


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
    audit_message = get_audit_message(audit_ntr_term_id)
    if 'term_id' in value:
        ontologyterm_id = value['@id']
        term_id = value['term_id']
        if term_id.startswith('NTR'):
            detail = f'{object_type} for {audit_link(path_to_text(ontologyterm_id), ontologyterm_id)} has been newly requested.'
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_ontology_term_object = {
    'audit_ntr_term_id': audit_ntr_term_id
}


@audit_checker('OntologyTerm', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_ontology_term_object.values()))
def audit_ontology_term_object_dispatcher(value, system):
    for function_name in function_dispatcher_ontology_term_object.keys():
        for failure in function_dispatcher_ontology_term_object[function_name](value, system):
            yield failure
