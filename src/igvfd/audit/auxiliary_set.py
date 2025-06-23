from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def audit_missing_measurement_sets(value, system):
    '''
    [
        {
            "audit_description": "Auxiliary sets are expected to be associated with a measurement set(s).",
            "audit_category": "missing measurement set",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_missing_measurement_sets)
    measurement_sets = value.get('measurement_sets', [])
    if not (measurement_sets):
        detail = (
            f'Auxiliary set {audit_link(path_to_text(value["@id"]), value["@id"])} is not '
            f'associated with any `measurement_sets`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_missing_barcode_map(value, system):
    '''
    [
        {
            "audit_description": "Cell hashing barcode sequencing auxiliary sets are expected to link to a barcode to hashtag mapping.",
            "audit_category": "missing barcode map",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Cell hashing barcode sequencing auxiliary sets are expected to link to only link to tabular file with content type of barcode to hashtag mapping.",
            "audit_category": "inconsistent barcode map",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing = get_audit_message(audit_missing_barcode_map, index=0)
    audit_message_inconsistent = get_audit_message(audit_missing_barcode_map, index=1)
    if value['file_set_type'] == 'cell hashing barcode sequencing':
        barcode_map = value.get('barcode_map', '')
        if not (barcode_map):
            detail = (
                f'Auxiliary set {audit_link(path_to_text(value["@id"]), value["@id"])} has '
                f'no `barcode_map`.'
            )
            yield AuditFailure(audit_message_missing.get('audit_category', ''), f'{detail} {audit_message_missing.get("audit_description", "")}', level=audit_message_missing.get('audit_level', ''))
        else:
            barcode_map_object = system.get('request').embed(barcode_map + '@@object?skip_calculated=true')
            if barcode_map_object['content_type'] != 'barcode to hashtag mapping':
                detail = (
                    f'Auxiliary set {audit_link(path_to_text(value["@id"]), value["@id"])} links '
                    f'to `barcode_map` {barcode_map} that is not a barcode to hashtag mapping.'
                )
                yield AuditFailure(audit_message_inconsistent.get('audit_category', ''), f'{detail} {audit_message_inconsistent.get("audit_description", "")}', level=audit_message_inconsistent.get('audit_level', ''))


function_dispatcher_auxiliary_set_object = {
    'audit_missing_measurement_sets': audit_missing_measurement_sets,
    'audit_missing_barcode_map': audit_missing_barcode_map
}


@audit_checker('AuxiliarySet', frame='object')
def audit_auxiliary_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_auxiliary_set_object.keys():
        for failure in function_dispatcher_auxiliary_set_object[function_name](value, system):
            yield failure
