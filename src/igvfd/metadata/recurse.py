from igvfd.metadata.constants import RECURSE_FILE_SET_LINK_FIELDS
from igvfd.metadata.constants import RECURSE_FILE_FIELDS


from pyramid.view import view_config


def extract_file_sets_and_files(file_set):
    file_sets = set()
    files = set()
    for link_field in RECURSE_FILE_SET_LINK_FIELDS:
        if link_field in file_set:
            value = file_set[link_field]
            if value:
                if isinstance(value, list):
                    file_sets.update(value)
                else:
                    file_sets.add(value)
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


def find_all_file_sets_and_files(request, file_set_at_ids):
    file_sets_seen = set()
    files_seen = set()
    file_sets = {
        at_id
        for at_id in file_set_at_ids
    }
    while file_sets:
        fs = file_sets.pop()
        if fs in file_sets_seen:
            continue
        file_sets_seen.add(fs)
        full_fs = request.embed(fs + '@@object')
        values = extract_file_sets_and_files(full_fs)
        for rfs in values['file_sets']:
            if rfs not in file_sets_seen:
                file_sets.add(rfs)
        files_seen.update(values['files'])
    return {
        'files': list(sorted(files_seen)),
        'file_sets': list(sorted(file_sets_seen)),
    }
