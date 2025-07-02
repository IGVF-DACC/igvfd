from .constants import FILE_SET_LINK_FIELDS
from .constants import FILE_FIELDS


def extract_file_sets_and_files(file_set):
    print('extracting file sets and files')
    file_sets = set()
    files = set()
    for link_field in FILE_SET_LINK_FIELDS:
        if link_field in file_set:
            print('found link field in fileset', link_field)
            value = file_set[link_field]
            print(value)
            if value:
                if isinstance(value, list):
                    file_sets.update(value)
                else:
                    file_sets.add(value)
    for field in FILE_FIELDS:
        if field in file_set:
            print('found file field', field)
            value = file_set[field]
            print(value)
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
        print('looking at fileset', fs)
        if fs in file_sets_seen:
            continue
        file_sets_seen.add(fs)
        full_fs = request.embed(fs + '@@object')
        print('Got full object')
        values = extract_file_sets_and_files(full_fs)
        print('Extracted values', values)
        for rfs in values['file_sets']:
            if rfs not in file_sets_seen:
                file_sets.add(rfs)
        files_seen.update(values['files'])
    return {
        'files': list(sorted(files_seen)),
        'file_sets': list(sorted(file_sets_seen)),
    }
