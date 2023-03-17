from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Sample', frame='object')
def audit_sample_sorted_fraction_parent_child_check(value, system):
    '''Samples that are a sorted_fraction of a parent sample should share
    most of the parent's metadata properties'''
    if 'sorted_fraction' in value:
        prop_errors = ''
        parent_id = value.get('sorted_fraction')
        parent = system.get('request').embed(parent_id + '@@object?skip_calculated=true')
        keys_to_check = [k for k in parent.keys() if k not in ['@context', '@id', '@type', 'accession', 'aliases', 'audit', 'creation_timestamp',
                                                               'date_obtained', 'schema_version', 'starting_amount', 'starting_amount_units', 'status', 'submitted_by', 'summary', 'uuid']]
        for key in keys_to_check:
            if value.get(key, '') != parent[key]:
                prop_errors += f'{key}, '
        detail = (
            f'Sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has metadata properties {prop_errors}inconsistent with '
            f'the associated parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
        )
        if prop_errors != '':
            yield AuditFailure('inconsistent sorted fraction metadata', detail, level='ERROR')
