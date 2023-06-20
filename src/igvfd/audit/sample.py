from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Sample', frame='object?skip_calculated=true')
def audit_sample_sorted_fraction_parent_child_check(value, system):
    '''Samples that are a sorted_fraction of a parent sample should share
    most of the parent's metadata properties'''
    if 'sorted_fraction' in value:
        error_keys = []
        prop_errors = ''
        value_id = system.get('path')
        parent_id = value.get('sorted_fraction')
        parent = system.get('request').embed(parent_id + '@@object?skip_calculated=true')
        skip_keys = ['accession', 'alternate_accessions', 'aliases', 'audit', 'creation_timestamp', 'date_obtained',
                     'schema_version', 'starting_amount', 'starting_amount_units', 'submitted_by', 'description',
                     'sorted_fraction', 'sorted_fraction_detail', 'revoke_detail', 'notes', 'submitter_comment',
                     'documents', 'url', 'dbxrefs', 'pooled_from', 'part_of', 'originated_from']
        all_keys = parent.keys() | value.keys()
        keys_to_check = [k for k in all_keys if k not in skip_keys]
        for key in keys_to_check:
            if value.get(key, None) != parent.get(key, None):
                error_keys.append(key)
        prop_errors = ', '.join(error_keys)
        detail = (
            f'Sample {audit_link(path_to_text(value_id), value_id)} '
            f'has metadata ({prop_errors}) inconsistent with '
            f'its associated parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
        )
        if prop_errors != '':
            yield AuditFailure('inconsistent sorted fraction metadata', detail, level='ERROR')


@audit_checker('Sample', frame='object')
def audit_sample_virtual_donor_check(value, system):
    '''Non-virtual samples should not be linked to virtual donors.'''
    if ('donors' in value) and (value.get('virtual', False) == False):
        sample_id = value['@id']
        donor_ids = value.get('donors', [])
        donors_error = []
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object')
            donor_id = donor_object.get('@id')
            donor_virtual = donor_object.get('virtual', False)
            if donor_virtual == True:
                donors_error.append(donor_id)

        if len(donors_error) > 0:
            detail = (f'The sample {audit_link(sample_id, sample_id)} is linked to virtual donor(s):'
                      f'{[audit_link(path_to_text(d_id),d_id) for d_id in donors_error]}')
            yield AuditFailure('inconsistent sample metadata', detail, level='ERROR')


@audit_checker('Sample', frame='object')
def audit_non_virtual_sample_linked_to_virtual_sample(value, system):
    '''Non-virtual samples should not be linked to virtual samples'''
    sample_id = system.get('path')
    sample_is_virtual = value.get('virtual', False)
    links_to_check = [
        value.get('part_of', None),
        value.get('originated_from', None),
        value.get('sorted_fraction', None),
    ]
    links_to_check.extend(value.get('pooled_from', []))
    for linked_sample in links_to_check:
        audit_failure = get_virtual_sample_failures(
            system,
            sample_id,
            sample_is_virtual,
            linked_sample
        )
        if audit_failure:
            yield audit_failure


def get_virtual_sample_failures(
    system,
    sample_id,
    sample_is_virtual,
    linked_sample_id
):
    if not linked_sample_id:
        return None
    linked_data = system.get('request').embed(linked_sample_id + '@@object?skip_calculated=true')
    if linked_data.get('virtual', False) != sample_is_virtual:
        if sample_is_virtual:
            audit_category = 'virtual sample linked to non-virtual sample'
            audit_detail_body = 'is virtual'
            audit_detail_end = 'that is not virtual'
        else:
            audit_category = 'non-virtual sample linked to virtual sample'
            audit_detail_body = 'is not virtual'
            audit_detail_end = 'that is virtual'
        detail = (
            f'Sample {audit_link(path_to_text(sample_id), sample_id)} '
            f'{audit_detail_body} and has a linked sample '
            f'({audit_link(path_to_text(linked_sample_id), linked_sample_id)}) {audit_detail_end}.'
        )
        return AuditFailure(audit_category, detail, level='ERROR')
    else:
        return None
