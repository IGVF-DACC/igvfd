from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('InVitroSystem', frame='object')
def audit_targeted_sample_term_check(value, system):
    '''
        audit_detail: In vitro systems are not expected to have the same targeted_sample_term and sample_terms.
        audit_category: inconsistent targeted_sample_term
        audit_levels: WARNING
    '''
    if 'targeted_sample_term' in value:
        value_id = system.get('path')
        sample_terms = value['sample_terms']
        targeted_sample_term = value['targeted_sample_term']
        for term in sample_terms:
            if term == targeted_sample_term:
                detail = (
                    f'InVitroSystem {audit_link(path_to_text(value_id), value_id)} '
                    f'has specified its targeted_sample_term to be the same as its sample_term.'
                )
                yield AuditFailure('inconsistent targeted_sample_term', detail, level='WARNING')


@audit_checker('InVitroSystem', frame='embedded')
def audit_cell_fate_change_treatments_purpose(value, system):
    '''
        audit_detail: Treatments linked to in an in vitro system's cell_fate_change_treatments are not expected to have purpose "perturbation", "agonist", "antagonist", or "control".
        audit_category: inconsistent cell_fate_change_treatments treatment purpose
        audit_levels: ERROR
    '''
    if 'cell_fate_change_treatments' in value:
        for treatment in value.get('cell_fate_change_treatments'):
            if treatment['purpose'] in ['perturbation', 'agonist', 'antagonist', 'control']:
                detail = (
                    f'InVitroSystem {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has cell_fate_change_treatment {audit_link(path_to_text(treatment["@id"]), treatment["@id"])} '
                    f'that has purpose {treatment["purpose"]}.'
                )
                yield AuditFailure('inconsistent cell_fate_change_treatments treatment purpose', detail, level='ERROR')
