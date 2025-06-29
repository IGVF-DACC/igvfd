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


def audit_targeted_sample_term_check(value, system):
    '''
    [
        {
            "audit_description": "In vitro systems are expected to have a targeted sample term that is distinct from the starting sample term.",
            "audit_category": "inconsistent targeted sample term",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_targeted_sample_term_check)
    if 'targeted_sample_term' in value:
        value_id = system.get('path')
        sample_terms = value['sample_terms']
        targeted_sample_term = value['targeted_sample_term']
        for term in sample_terms:
            if term == targeted_sample_term:
                detail = (
                    f'In vitro system {audit_link(path_to_text(value_id), value_id)} '
                    f'has specified its `targeted_sample_term` to be the same as in `sample_terms`.'
                )
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_cell_fate_change_protocol_document_type(value, system):
    '''
    [
        {
            "audit_description": "A document listed as a cell fate change protocol is expected to have a cell fate change protocol document type.",
            "audit_category": "inconsistent document type",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_cell_fate_change_protocol_document_type)
    if 'cell_fate_change_protocol' in value:
        doc_object = system.get('request').embed(value['cell_fate_change_protocol'] + '@@object?skip_calculated=true')
        if doc_object['document_type'] != 'cell fate change protocol':
            detail = (
                f'In vitro system {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a protocol {audit_link(path_to_text(value["cell_fate_change_protocol"]), value["cell_fate_change_protocol"])} in `cell_fate_change_protocols` '
                f'that does not have `document_type` cell fate change protocol.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_in_vitro_system_object = {
    'audit_targeted_sample_term_check': audit_targeted_sample_term_check
}

function_dispatcher_in_vitro_system_embedded = {
    'audit_cell_fate_change_protocol_document_type': audit_cell_fate_change_protocol_document_type
}


@audit_checker('InVitroSystem', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_in_vitro_system_object.values()))
def audit_in_vitro_system_object_dispatcher(value, system):
    for function_name in function_dispatcher_in_vitro_system_object.keys():
        for failure in function_dispatcher_in_vitro_system_object[function_name](value, system):
            yield failure


@audit_checker('InVitroSystem', frame='embedded')
@watch_for_changes_in(functions=list(function_dispatcher_in_vitro_system_embedded.values()))
def audit_in_vitro_system_embedded_dispatcher(value, system):
    for function_name in function_dispatcher_in_vitro_system_embedded.keys():
        for failure in function_dispatcher_in_vitro_system_embedded[function_name](value, system):
            yield failure
