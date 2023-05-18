from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Tissue', frame='object')
def audit_tissue_ccf_id(value, system):
    '''Tissue objects must specify a common coordinate framework identifier (CCF ID) required for human data.'''
    if ('ccf_id' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'is missing common coordinate framework identifier (CCF ID) required for human data.'
        )
        yield AuditFailure('missing ccf_id', detail, level='NOT_COMPLIANT')


@audit_checker('Tissue', frame='object')
def audit_tissue_age(value, system):
    '''Tissue objects must specify a lower_bound_age, upper_bound_age and age_units.'''
    if 'lower_bound_age' and 'upper_bound_age' and 'age_units' not in value:
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'is missing upper_bound_age, lower_bound_age, and age_units.'
        )
        yield AuditFailure('missing age properties', detail, level='WARNING')
