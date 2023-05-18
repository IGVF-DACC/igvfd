from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('WholeOrganism', frame='object')
def audit_whole_organism_human_taxa(value, system):
    '''Flag whole organisms associated with taxa Homo sapiens.'''
    detail = (
        f'Whole organism {audit_link(path_to_text(value["@id"]), value["@id"])} '
        f'specifies that it is of taxa Homo sapiens, this is disallowed.'
    )
    if 'taxa' in value:
        if value['taxa'] == 'Homo sapiens':
            yield AuditFailure('incorrect taxa', detail, level='ERROR')
    elif 'donors' in value:
        donor_ids = value.get('donors')
        taxa_set = set()
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            taxa_set.add(donor_object.get('taxa', ''))
        if 'Homo sapiens' in taxa_set:
            yield AuditFailure('incorrect taxa', detail, level='ERROR')


@audit_checker('WholeOrganism', frame='object')
def audit_tissue_age(value, system):
    '''WholeOrganism must specify a lower_bound_age, upper_bound_age and age_units.'''
    if 'lower_bound_age' and 'upper_bound_age' and 'age_units' not in value:
        value_id = system.get('path')
        detail = (
            f'WholeOrganism {audit_link(path_to_text(value_id), value_id)} '
            f'is missing upper_bound_age, lower_bound_age, and age_units.'
        )
        yield AuditFailure('missing age properties', detail, level='WARNING')
