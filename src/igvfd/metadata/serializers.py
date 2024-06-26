from snovault.util import simple_path_ids
from igvfd.metadata.constants import BOOLEAN_MAP


def make_experiment_cell(paths, experiment):
    last = []
    for path in paths:
        cell_value = []
        for value in simple_path_ids(experiment, path):
            if str(value) not in cell_value:
                cell_value.append(str(value))
        if last and cell_value:
            last = [
                v + ' ' + cell_value[0]
                for v in last
            ]
        else:
            last = cell_value
    return ', '.join(set(last))


def make_file_cell(paths, file_):
    # Quick return if one level deep.
    if len(paths) == 1 and '.' not in paths[0]:
        value = file_.get(paths[0], '')
        if isinstance(value, list):
            return ', '.join([str(v) for v in value])
        return value
    # Else crawl nested objects.
    last = []
    for path in paths:
        cell_value = []
        for value in simple_path_ids(file_, path):
            cell_value.append(str(value))
        if last and cell_value:
            last = [
                v + ' ' + cell_value[0]
                for v in last
            ]
        else:
            last = cell_value
    return ', '.join(sorted(set(last)))


def maybe_int(value):
    try:
        return int(value.replace('_', ' '))
    except Exception:
        return value


def map_string_to_boolean_and_int(value):
    return BOOLEAN_MAP.get(value, maybe_int(value))


def map_strings_to_booleans_and_ints(values):
    return [
        map_string_to_boolean_and_int(v)
        for v in values
    ]
