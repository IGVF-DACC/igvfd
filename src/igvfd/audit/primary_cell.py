from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('PrimaryCell', frame='object')
def audit_tissue_age(value, system):
    '''PrimaryCell objects must specify a lower_bound_age, upper_bound_age and age_units.'''
    if 'lower_bound_age' and 'upper_bound_age' and 'age_units' not in value:
        value_id = system.get('path')
        detail = (
            f'PrimaryCell {audit_link(path_to_text(value_id), value_id)} '
            f'is missing upper_bound_age, lower_bound_age, and age_units.'
        )
        yield AuditFailure('missing age properties', detail, level='WARNING')
