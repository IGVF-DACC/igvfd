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
    '''Flag biosamples if targeted_sample_term and biosample_term is the same'''

    if 'targeted_sample_term' in value:
        value_id = system.get('path')
        biosample_term = value['biosample_term']
        targeted_sample_term = value['targeted_sample_term']
        if biosample_term == targeted_sample_term:
            detail = (
                f'InVitroSystem {audit_link(path_to_text(value_id), value_id)} '
                f'has specified its targeted_sample_term to be the same as its sample_term.'
            )
            yield AuditFailure('inconsistent targeted_sample_term', detail, level='WARNING')
