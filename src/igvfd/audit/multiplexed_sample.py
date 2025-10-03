from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def audit_multiplexed_sample_no_barcode_map(value, system):
    '''
    [
        {
            "audit_description": "Multiplexed samples that use barcodes for demultiplexing are expected to specify a barcode map.",
            "audit_category": "missing barcode map",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_multiplexed_sample_no_barcode_map, index=0)

    detail = (
        f'Multiplexed sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
        f'has no `barcode_map`.'
    )
    if 'barcode based' in value['multiplexing_methods']:
        barcode_map = value.get('barcode_map', '')
        if not (barcode_map):
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
        else:
            barcode_map_obj = system.get('request').embed(barcode_map, '@@object?skip_calculated=true')
            if barcode_map_obj['content_type'] != 'barcode to sample mapping':
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_multiplexed_sample_object = {
    'audit_multiplexed_sample_no_barcode_map': audit_multiplexed_sample_no_barcode_map
}


@audit_checker('MultiplexedSample', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_multiplexed_sample_object.values()))
def audit_multiplexed_sample_object_dispatcher(value, system):
    for function_name in function_dispatcher_multiplexed_sample_object.keys():
        for failure in function_dispatcher_multiplexed_sample_object[function_name](value, system):
            yield failure
