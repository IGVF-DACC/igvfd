from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description,
)


@audit_checker('InVitroSystem', frame='object')
def audit_targeted_sample_term_check(value, system):
    '''
    [
        {
            "audit_description": "In vitro systems are expected to have a targeted sample term that is distinct from the starting sample term.",
            "audit_category": "inconsistent targeted sample term",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_targeted_sample_term_check)
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
                yield AuditFailure('inconsistent targeted sample term', f'{detail} {description}', level='WARNING')


@audit_checker('InVitroSystem', frame='embedded')
def audit_cell_fate_change_treatments_purpose(value, system):
    '''
    [
        {
            "audit_description": "Cell fate change treatments are expected to have a purpose associated with cell fate change.",
            "audit_category": "inconsistent treatment purpose",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_cell_fate_change_treatments_purpose)
    if 'cell_fate_change_treatments' in value:
        for treatment in value.get('cell_fate_change_treatments'):
            if treatment['purpose'] in ['perturbation', 'agonist', 'antagonist', 'control']:
                detail = (
                    f'In vitro system {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has a treatment {audit_link(path_to_text(treatment["@id"]), treatment["@id"])} in `cell_fate_change_treatments` '
                    f'that has `purpose` {treatment["purpose"]}.'
                )
                yield AuditFailure('inconsistent treatment purpose', f'{detail} {description}', level='WARNING')


@audit_checker('InVitroSystem', frame='embedded')
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
    description = get_audit_description(audit_cell_fate_change_protocol_document_type)
    if 'cell_fate_change_protocol' in value:
        doc_object = system.get('request').embed(value['cell_fate_change_protocol'] + '@@object?skip_calculated=true')
        if doc_object['document_type'] != 'cell fate change protocol':
            detail = (
                f'In vitro system {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a protocol {audit_link(path_to_text(value["cell_fate_change_protocol"]), value["cell_fate_change_protocol"])} in `cell_fate_change_protocols` '
                f'that does not have `document_type` "cell fate change protocol".'
            )
            yield AuditFailure('inconsistent document type', f'{detail} {description}', level='ERROR')
