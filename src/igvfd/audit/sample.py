from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)

# Flag samples that have sorted fraction relationships but do not have matching properties


def audit_sample_sorted_fractions(value, system):
    print('audit_sample_sorted_fractions ran...')
    sorted_fraction_value = value.get('sorted_fraction')
    if sorted_fraction_value is not None:
        value_source = value.get('source')
        value_lot_id = value.get('lot_id')
        value_product_id = value.get('product_id')
        sorted_fraction_source = sorted_fraction_value.get('source')
        sorted_fraction_lot_id = sorted_fraction_value.get('lot_id')
        sorted_fraction_product_id = sorted_fraction_value.get('product_id')
        if value_source != sorted_fraction_source:
            detail = (
                f'Sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has product info source {value_source}, yet '
                f'the associated sorted fraction {audit_link(path_to_text(sorted_fraction_value["@id"]), sorted_fraction_value["@id"])} '
                f'has product info source {sorted_fraction_source}.'
            )
            yield AuditFailure('inconsistent product info source', detail, level='WARNING')
        if value_lot_id != sorted_fraction_lot_id:
            detail = (
                f'Sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has product info lot ID {value_lot_id}, yet '
                f'the associated sorted fraction {audit_link(path_to_text(sorted_fraction_value["@id"]), sorted_fraction_value["@id"])} '
                f'has product info lot ID {sorted_fraction_lot_id}.'
            )
            yield AuditFailure('inconsistent product info lot ID', detail, level='WARNING')
        if value_product_id != sorted_fraction_product_id:
            detail = (
                f'Sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has product info product ID {value_product_id}, yet '
                f'the associated sorted fraction {audit_link(path_to_text(sorted_fraction_value["@id"]), sorted_fraction_value["@id"])} '
                f'has product info product ID {sorted_fraction_product_id}.'
            )
            yield AuditFailure('inconsistent product info product ID', detail, level='WARNING')


function_dispatcher = {
    'audit_sample_sorted_fractions': audit_sample_sorted_fractions,
}


@audit_checker('Sample', frame=['{sorted_fraction}'])
def audit_sample(value, system):
    print('audit_sample ran...')
    for function_name in function_dispatcher.keys():
        for failure in function_dispatcher[function_name](value, system):
            yield failure
