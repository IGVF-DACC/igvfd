from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)
from .compare_dict_values import (
    compare_dictionary
)


items_to_not_compare = [
    '@context',
    '@id',
    '@type',
    'accession',
    'aliases',
    'audit',
    'creation_timestamp',
    'date_obtained',
    'schema_version',
    'starting_amount',
    'starting_amount_units',
    'status',
    'submitted_by',
    'summary',
    'uuid',
    'sorted_fraction']


def audit_sample_sorted_fractions(child_value, system):
    child_id = child_value['@id']
    parent_id = child_value.get('sorted_fraction')
    if parent_id is not None:
        request = system.get('request')
        parent_value = request.embed(parent_id + '@@object')
        differences = compare_dictionary(
            child_value,
            parent_value,
            items_to_not_compare)
        if len(differences) > 0:
            is_first_item = True
            key_diffs_msg = ''
            for current_key in differences:
                if is_first_item:
                    is_first_item = False
                else:
                    key_diffs_msg += ', '
                key_diffs_msg += current_key
            detail = (
                f'Sample {audit_link(path_to_text(child_id), child_id)} is different from '
                f'the associated parent sample {audit_link(path_to_text(parent_id), parent_id)} '
                f'because the following properties are different: {key_diffs_msg}'
            )
            yield AuditFailure('sorted fraction inconsistent', detail, level='ERROR')


function_dispatcher = {
    'audit_sample_sorted_fractions': audit_sample_sorted_fractions,
}


@audit_checker('Sample', frame='object')
def audit_sample(value, system):
    for function_name in function_dispatcher.keys():
        for failure in function_dispatcher[function_name](value, system):
            yield failure
