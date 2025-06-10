from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, run_audits


@register_audit(['MultiplexedSample'], frame='object')
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

    if 'barcode based' in value['multiplexing_methods']:
        if not (value.get('barcode_map')):
            detail = (
                f'Multiplexed sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has no `barcode_map`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MultiplexedSample', frame='object')
def audit_multiplexed_sample_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')
