from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('MultiplexedSample', frame='object')
def audit_multiplexed_sample_no_barcode_map(value, system):
    '''
    [
        {
            "audit_description": "Multiplexed samples that use barcodes for demultiplexing are expected to specify a barcode sample map.",
            "audit_category": "missing barcode sample map",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_multiplexed_sample_no_barcode_map, index=0)
    if not (value.get('barcode_sample_map')):
        detail = (
            f'Multiplexed sample {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `barcode_sample_map`.'
        )
        yield AuditFailure('missing barcode sample map', f'{detail} {description}', level='WARNING')
