from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)
from .compare_dict_values import (
    DictDifference,
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
        for difference in differences:
            if difference.item_1_value is None:
                detail = (
                    f'Sample {audit_link(path_to_text(child_id), child_id)} '
                    f'does not have property {difference.item_key} which is different from '
                    f'the associated parent sample {audit_link(path_to_text(parent_id), parent_id)} '
                    f'where it has property {difference.item_key}: {difference.item_2_value}.'
                )
                yield AuditFailure('sorted fraction child missing ' + difference.item_key, detail, level='ERROR')
            if difference.item_2_value is None:
                detail = (
                    f'Sample {audit_link(path_to_text(child_id), child_id)} '
                    f'has property {difference.item_key}: {difference.item_1_value} that is different from '
                    f'the associated parent sample {audit_link(path_to_text(parent_id), parent_id)} '
                    f'where it is missing the property {difference.item_key}.'
                )
                yield AuditFailure('sorted fraction parent missing ' + difference.item_key, detail, level='ERROR')
            if (difference.item_1_value is not None) and (difference.item_2_value is not None):
                detail = (
                    f'Sample {audit_link(path_to_text(child_id), child_id)} '
                    f'has property {difference.item_key}: {difference.item_1_value} that is different from '
                    f'the associated parent sample {audit_link(path_to_text(parent_id), parent_id)} '
                    f'where it has property {difference.item_key}: {difference.item_2_value}.'
                )
                yield AuditFailure('sorted fraction inconsistent ' + difference.item_key, detail, level='ERROR')


function_dispatcher = {
    'audit_sample_sorted_fractions': audit_sample_sorted_fractions,
}


@audit_checker('Sample', frame='object')
def audit_sample(value, system):
    for function_name in function_dispatcher.keys():
        for failure in function_dispatcher[function_name](value, system):
            yield failure
