from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words,
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


def audit_term_id_not_in_ontology(value, system):
    '''
    [
        {
            "audit_description": "Term identifiers for ontology terms are expected to exist in the reference ontology database.",
            "audit_category": "missing ontology reference",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    audit_message = get_audit_message(audit_term_id_not_in_ontology)
    object_type = space_in_words(value['@type'][0]).capitalize()
    ontology = system['registry']['ontology']
    term_id = value['term_id']
    ontologyterm_id = value['@id']

    if term_id not in ontology:
        prefix = term_id.split(':', 1)[0]
        detail = (
            f'{object_type} {audit_link(path_to_text(ontologyterm_id), ontologyterm_id)} specifies '
            f'a `term_id` {term_id} that is not part of the {prefix} ontology.'
        )
        yield AuditFailure(
            audit_message.get('audit_category', ''),
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_message.get('audit_level', ''),
        )


def audit_inconsistent_ontology_term(value, system):
    '''
    [
        {
            "audit_description": "The term name is expected to match the canonical name or a synonym in the reference ontology for the given term identifier.",
            "audit_category": "inconsistent ontology term",
            "audit_level": "ERROR"
        }
    ]
    '''
    if value['term_id'].startswith('NTR'):
        return
    ontology = system['registry']['ontology']
    term_id = value['term_id']
    term_name = value['term_name']
    if term_id not in ontology:
        return
    ontology_entry = ontology[term_id]
    ontology_term_name = ontology_entry.get('name')
    if ontology_term_name == term_name:
        return

    audit_message = get_audit_message(audit_inconsistent_ontology_term)
    object_type = space_in_words(value['@type'][0]).capitalize()
    ontologyterm_id = value['@id']
    detail = (
        f'{object_type} {audit_link(path_to_text(ontologyterm_id), ontologyterm_id)} has a mismatch between '
        f'`term_id` ({term_id}) and `term_name` ({term_name}); '
        f'the ontology name for {term_id} is {ontology_term_name!r}.'
    )
    yield AuditFailure(
        audit_message.get('audit_category', ''),
        f'{detail} {audit_message.get("audit_description", "")}',
        level=audit_message.get('audit_level', ''),
    )


function_dispatcher_ontology_term_object = {
    'audit_ntr_term_id': audit_ntr_term_id,
    'audit_term_id_not_in_ontology': audit_term_id_not_in_ontology,
    'audit_inconsistent_ontology_term': audit_inconsistent_ontology_term,
}


@audit_checker('OntologyTerm', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_ontology_term_object.values()))
def audit_ontology_term_object_dispatcher(value, system):
    for function_name in function_dispatcher_ontology_term_object.keys():
        for failure in function_dispatcher_ontology_term_object[function_name](value, system):
            yield failure
