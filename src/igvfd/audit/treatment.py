from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


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
    audit_message = get_audit_message(audit_treatment_term_id_check)
    if 'treatment_term_id' in value:
        term_id = value['treatment_term_id']
        if term_id.startswith('NTR'):
            treatment_id = value['@id']
            detail = f'Treatment term for {audit_link(path_to_text(treatment_id), treatment_id)} has been newly requested.'
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_treatment_object = {
    'audit_treatment_term_id_check': audit_treatment_term_id_check
}


@audit_checker('Treatment', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_treatment_object.values()))
def audit_treatment_object_dispatcher(value, system):
    for function_name in function_dispatcher_treatment_object.keys():
        for failure in function_dispatcher_treatment_object[function_name](value, system):
            yield failure
