from igvfd.metadata.constants import RECURSE_FILE_SET_FIELDS
from igvfd.metadata.constants import RECURSE_FILE_SET_DOWNSTREAM_FIELDS
from igvfd.metadata.constants import RECURSE_FILE_FIELDS


from pyramid.view import view_config


def extract_related_file_sets_and_files(full_file_set, can_downstream):
    related_file_sets = set()
    files = set()
    file_set_type = full_file_set['@type'][0]
    for link_field in RECURSE_FILE_SET_FIELDS.get(file_set_type, []):
        if link_field not in full_file_set:
            continue
        value = full_file_set[link_field]
        if value:
            if isinstance(value, list):
                related_file_sets.update((v, False) for v in value)
            else:
                related_file_sets.add((value, False))
    if can_downstream:
        for link_field in RECURSE_FILE_SET_DOWNSTREAM_FIELDS.get(file_set_type, []):
            if link_field not in full_file_set:
                continue
            value = full_file_set[link_field]
            if value:
                if isinstance(value, list):
                    related_file_sets.update((v, True) for v in value)
            else:
                related_file_sets.add((value, True))
    for field in RECURSE_FILE_FIELDS:
        if field in full_file_set:
            value = full_file_set[field]
            if value:
                if isinstance(value, list):
                    files.update(value)
                else:
                    files.add(value)
    return {
        'related_file_sets': related_file_sets,
        'files': files,
    }


def find_all_file_sets_and_files(request, file_set_at_ids, include_downstream=False):
    file_sets_seen = set()
    files_seen = set()
    file_sets = {
        (file_set_at_id, include_downstream)
        for file_set_at_id in file_set_at_ids
    }
    while file_sets:
        file_set_at_id, can_downstream = file_sets.pop()
        if (file_set_at_id, can_downstream) in file_sets_seen:
            continue
        file_sets_seen.add((file_set_at_id, can_downstream))
        full_file_set = request.embed(file_set_at_id + '@@object')
        values = extract_related_file_sets_and_files(full_file_set, can_downstream)
        for related_file_set in values['related_file_sets']:
            if related_file_set not in file_sets_seen:
                file_sets.add(related_file_set)
        files_seen.update(values['files'])
    file_sets_seen = {
        file_set_at_id
        for file_set_at_id, can_downstream in file_sets_seen
    }
    return {
        'files': sorted(files_seen),
        'file_sets': sorted(file_sets_seen),
    }
