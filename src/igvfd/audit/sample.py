from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


def audit_sample_sorted_from_parent_child_check(value, system):
    '''
    [
        {
            "audit_description": "Samples that are sorted from or part of a parent sample are expected to share most of the parent's metadata properties.",
            "audit_category": "inconsistent parent sample",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Samples are expected to be either sorted from or part of another sample, but never both.",
            "audit_category": "inconsistent parent sample",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(system.get('types')[0]).capitalize()
    audit_message_metadata_inconsistency = get_audit_message(audit_sample_sorted_from_parent_child_check, index=0)
    audit_message_duplicated_parent = get_audit_message(audit_sample_sorted_from_parent_child_check, index=1)
    if 'sorted_from' in value or 'part_of' in value:
        inconsistent_properties = []
        missing_properties = []
        value_id = system.get('path')
        if 'sorted_from' in value:
            parent_id = value.get('sorted_from')
        elif 'part_of' in value:
            parent_id = value.get('part_of')
        if 'sorted_from' in value and 'part_of' in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value_id), value_id)} '
                f'specifies both `sorted_from` and `part_of`.'
            )
            yield AuditFailure(audit_message_duplicated_parent.get('audit_category', ''), f'{detail} {audit_message_duplicated_parent.get("audit_description", "")}', level=audit_message_duplicated_parent.get('audit_level', ''))
        parent = system.get('request').embed(parent_id + '@@object?skip_calculated=true')
        skip_keys = ['accession', 'aliases', 'alternate_accessions', 'audit', 'cellular_sub_pool', 'creation_timestamp', 'date_obtained', 'dbxrefs', 'description', 'documents', 'notes', 'originated_from', 'part_of',
                     'pooled_from', 'release_timestamp', 'revoke_detail', 'schema_version', 'sorted_from', 'sorted_from_detail', 'starting_amount', 'starting_amount_units', 'submitter_comment', 'submitted_by', 'treatments', 'url']
        all_keys = parent.keys() | value.keys()
        keys_to_check = [key for key in all_keys if key not in skip_keys]
        for key in keys_to_check:
            if key not in value:
                missing_properties.append(key)
            elif key not in parent:
                inconsistent_properties.append(key)
            elif value[key] != parent[key]:
                inconsistent_properties.append(key)
        inconsistent_properties = ', '.join([f'`{key}`' for key in inconsistent_properties])
        missing_properties = ', '.join([f'`{key}`' for key in missing_properties])
        if inconsistent_properties:
            detail = (
                f'{object_type} {audit_link(path_to_text(value_id), value_id)} '
                f'has metadata properties ({inconsistent_properties}) inconsistent with '
                f'its associated parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
            )
            yield AuditFailure(audit_message_metadata_inconsistency.get('audit_category', ''), f'{detail} {audit_message_metadata_inconsistency.get("audit_description", "")}', level=audit_message_metadata_inconsistency.get('audit_level', ''))
        if missing_properties:
            detail = (
                f'{object_type} {audit_link(path_to_text(value_id), value_id)} '
                f'is missing metadata properties ({missing_properties}) which are '
                f'associated with the parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
            )
            yield AuditFailure(audit_message_metadata_inconsistency.get('audit_category', ''), f'{detail} {audit_message_metadata_inconsistency.get("audit_description", "")}', level=audit_message_metadata_inconsistency.get('audit_level', ''))


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
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_sample_virtual_donor_check)
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
            detail = (f'{object_type} {audit_link(path_to_text(sample_id), sample_id)} is linked to virtual `donors`: '
                      f'{donors_to_link}.')
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_non_virtual_sample_linked_to_virtual_sample)
    sample_is_virtual = value.get('virtual', False)
    links_to_check = [v for v in [
        value.get('part_of'),
        value.get('originated_from'),
        value.get('sorted_from'),
    ] if v]
    links_to_check.extend(value.get('pooled_from', []))
    for linked_sample_id in links_to_check:
        linked_data = system.get('request').embed(linked_sample_id + '@@object?skip_calculated=true')
        linked_is_virtual = linked_data.get('virtual', False)
        if linked_is_virtual != sample_is_virtual:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'{"is virtual" if sample_is_virtual else "is not virtual"} and has a linked sample '
                f'{audit_link(path_to_text(linked_sample_id), linked_sample_id)} '
                f'{"that is not virtual" if sample_is_virtual else "that is virtual"}.'
            )
            yield AuditFailure(
                audit_message.get('audit_category', ''),
                f'{detail} {audit_message.get("audit_description", "")}',
                level=audit_message.get('audit_level', '')
            )


def audit_parent_sample_with_singular_child(value, system):
    '''
    [
        {
            "audit_description": "Parent samples are expected to have multiple child samples.",
            "audit_category": "missing sample",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_parent_sample_with_singular_child)
    for child_sample_type in ['parts', 'origin_of', 'sorted_fractions']:
        if child_sample_type in value and len(value.get(child_sample_type, [])) == 1:
            child_sample = value.get(child_sample_type)[0]
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has only 1 child sample {audit_link(path_to_text(child_sample), child_sample)} '
                f'in `{child_sample_type}`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_missing_nucleic_acid_delivery(value, system):
    '''
    [
        {
            "audit_description": "Samples linked to construct library sets are expected to specify nucleic acid delivery method.",
            "audit_category": "missing nucleic acid delivery",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_missing_nucleic_acid_delivery)
    if 'construct_library_sets' in value and 'nucleic_acid_delivery' not in value:
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `construct_library_sets` but is missing `nucleic_acid_delivery`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_sample_missing_publication(value, system):
    '''
    [
        {
            "audit_description": "Released and archived samples are expected to be associated with a publication.",
            "audit_category": "missing publication",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_sample_missing_publication, index=0)
    if value.get('status') in ['released', 'archived'] and not (value.get('publications')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `publications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_missing_association(value, system):
    '''
    [
        {
            "audit_description": "Samples are expected to be associated with another sample or file set.",
            "audit_category": "missing association",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_missing_association)
    properties = ['file_sets', 'origin_of', 'parts', 'sorted_fractions', 'multiplexed_in', 'pooled_in']
    if all(not value.get(prop) for prop in properties):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'is not associated with any file set, nor is the parent of any sample.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_sample_skip_calculated = {
    'audit_sample_sorted_from_parent_child_check': audit_sample_sorted_from_parent_child_check
}

function_dispatcher_sample_object = {
    'audit_sample_virtual_donor_check': audit_sample_virtual_donor_check,
    'audit_non_virtual_sample_linked_to_virtual_sample': audit_non_virtual_sample_linked_to_virtual_sample,
    'audit_parent_sample_with_singular_child': audit_parent_sample_with_singular_child,
    'audit_missing_nucleic_acid_delivery': audit_missing_nucleic_acid_delivery,
    'audit_sample_missing_publication': audit_sample_missing_publication,
    'audit_missing_association': audit_missing_association
}


@audit_checker('Sample', frame='object?skip_calculated=true')
@watch_for_changes_in(functions=list(function_dispatcher_sample_skip_calculated.values()))
def audit_sample_skip_calculated_dispatcher(value, system):
    for function_name in function_dispatcher_sample_skip_calculated.keys():
        for failure in function_dispatcher_sample_skip_calculated[function_name](value, system):
            yield failure


@audit_checker('Sample', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_sample_object.values()))
def audit_sample_object_dispatcher(value, system):
    for function_name in function_dispatcher_sample_object.keys():
        for failure in function_dispatcher_sample_object[function_name](value, system):
            yield failure
