from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('Sample', frame='object?skip_calculated=true')
def audit_sample_sorted_from_parent_child_check(value, system):
    '''
    [
        {
            "audit_description": "Samples that are sorted from a parent sample are expected to share most of the parent's metadata properties.",
            "audit_category": "inconsistent parent sample",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_sample_sorted_from_parent_child_check)
    if 'sorted_from' in value:
        error_keys = []
        prop_errors = ''
        value_id = system.get('path')
        parent_id = value.get('sorted_from')
        parent = system.get('request').embed(parent_id + '@@object?skip_calculated=true')
        skip_keys = ['accession', 'alternate_accessions', 'aliases', 'audit', 'creation_timestamp', 'date_obtained',
                     'schema_version', 'starting_amount', 'starting_amount_units', 'submitted_by', 'description',
                     'sorted_from', 'sorted_from_detail', 'revoke_detail', 'notes', 'submitter_comment',
                     'documents', 'url', 'dbxrefs', 'pooled_from', 'part_of', 'originated_from', 'release_timestamp']
        all_keys = parent.keys() | value.keys()
        keys_to_check = [k for k in all_keys if k not in skip_keys]
        for key in keys_to_check:
            if value.get(key, None) != parent.get(key, None):
                error_keys.append(key)
        prop_errors = '`, `'.join(error_keys)
        detail = (
            f'Sample {audit_link(path_to_text(value_id), value_id)} '
            f'has metadata properties ({prop_errors}) inconsistent with '
            f'its associated parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
        )
        if prop_errors != '':
            yield AuditFailure('inconsistent parent sample', f'{detail} {description}', level='ERROR')


@audit_checker('Sample', frame='object')
def audit_sample_virtual_donor_check(value, system):
    '''
    [
        {
            "audit_description": "Non-virtual samples are expected to be derived from non-virtual donors.",
            "audit_category": "inconsistent donor",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_sample_virtual_donor_check)
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
        donors_to_link = [audit_link(path_to_text(d_id), d_id) for d_id in donors_error]
        donors_to_link = ', '.join(donors_to_link)
        if len(donors_error) > 0:
            detail = (f'Sample {audit_link(path_to_text(sample_id), sample_id)} is linked to virtual `donors`: '
                      f'{donors_to_link}')
            yield AuditFailure('inconsistent donor', f'{detail} {description}', level='ERROR')


@audit_checker('Sample', frame='object')
def audit_non_virtual_sample_linked_to_virtual_sample(value, system):
    '''
    [
        {
            "audit_description": "Non-virtual samples are expected to be derived from non-virtual samples.",
            "audit_category": "inconsistent parent sample",
            "audit_level": "ERROR"
        }
    ]
    '''
    sample_id = system.get('path')
    sample_is_virtual = value.get('virtual', False)
    links_to_check = [item for item in [
        value.get('part_of', None),
        value.get('originated_from', None),
        value.get('sorted_from', None),
    ] if item is not None]
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
    description = get_audit_description(audit_non_virtual_sample_linked_to_virtual_sample)
    linked_data = system.get('request').embed(linked_sample_id + '@@object?skip_calculated=true')
    if linked_data.get('virtual', False) != sample_is_virtual:
        if sample_is_virtual:
            audit_detail_body = 'is virtual'
            audit_detail_end = 'that is not virtual'
        else:
            audit_detail_body = 'is not virtual'
            audit_detail_end = 'that is virtual'
        detail = (
            f'Sample {audit_link(path_to_text(sample_id), sample_id)} '
            f'{audit_detail_body} and has a linked sample '
            f'{audit_link(path_to_text(linked_sample_id), linked_sample_id)} {audit_detail_end}.'
        )
        return AuditFailure('inconsistent parent sample', f'{detail} {description}', level='ERROR')
    else:
        return None


@audit_checker('Sample', frame='object')
def audit_construct_library_sets_types(value, system):
    '''
    [
        {
            "audit_description": "Samples are expected to link to a construct library sets with the same file set type.",
            "audit_category": "inconsistent construct library sets",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_sets_types)
    if 'construct_library_sets' in value and len(value['construct_library_sets']) > 1:
        library_types = set()
        for CLS in value['construct_library_sets']:
            CLS_object = system.get('request').embed(CLS, '@@object?skip_calculated=true')
            library_types.add(CLS_object['file_set_type'])
        if len(library_types) > 1:
            if len(library_types) > 2:
                library_types = list(library_types)
                library_types = ', and '.join([', '.join(library_types[:-1]), library_types[-1]])
            else:
                library_types = ' and '.join(library_types)
            detail = (
                f'Sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has `construct_library_sets` of multiple types {library_types}.'
            )
            yield AuditFailure('inconsistent construct library sets', f'{detail} {description}', level='WARNING')
