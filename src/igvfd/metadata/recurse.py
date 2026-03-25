from igvfd.metadata.constants import RECURSE_FILE_SET_FIELDS
from igvfd.metadata.constants import RECURSE_FILE_SET_DOWNSTREAM_FIELDS
from igvfd.metadata.constants import RECURSE_FILE_FIELDS


from pyramid.view import view_config


def extract_file_sets_and_files(file_set, can_downstream):
    file_sets = set()
    files = set()
    file_set_type = file_set['@type'][0]
    for link_field in RECURSE_FILE_SET_FIELDS.get(file_set_type, []):
        if link_field not in file_set:
            continue
        value = file_set[link_field]
        if value:
            if isinstance(value, list):
                file_sets.update((v, False) for v in value)
            else:
                file_sets.add((value, False))
    if can_downstream:
        for link_field in RECURSE_FILE_SET_DOWNSTREAM_FIELDS.get(file_set_type, []):
            if link_field not in file_set:
                continue
            value = file_set[link_field]
            if value:
                if isinstance(value, list):
                    file_sets.update((v, True) for v in value)
            else:
                file_sets.add((value, True))
    for field in RECURSE_FILE_FIELDS:
        if field in file_set:
            value = file_set[field]
            if value:
                if isinstance(value, list):
                    files.update(value)
                else:
                    files.add(value)
    return {
        'file_sets': file_sets,
        'files': files,
    }


def find_all_file_sets_and_files(request, file_set_at_ids, include_downstream=False):
    file_sets_seen = set()
    files_seen = set()
    file_sets = {
        (at_id, include_downstream)
        for at_id in file_set_at_ids
    }
    while file_sets:
        fs, can_downstream = file_sets.pop()
        if (fs, can_downstream) in file_sets_seen:
            continue
        file_sets_seen.add((fs, can_downstream))
        full_fs = request.embed(fs + '@@object')
        values = extract_file_sets_and_files(full_fs, can_downstream)
        for rfs in values['file_sets']:
            if rfs not in file_sets_seen:
                file_sets.add(rfs)
        files_seen.update(values['files'])
    file_sets_seen = {
        fs
        for fs, can_downstream in file_sets_seen
    }
    return {
        'files': sorted(files_seen),
        'file_sets': sorted(file_sets_seen),
    }
