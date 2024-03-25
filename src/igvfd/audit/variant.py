from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Variant', frame='object')
def audit_variant_ref_alt_check(value, system):
    '''
    [
        {
            "audit_description": "Variants are expected to have a different reference allele and alternative allele.",
            "audit_category": "identical alleles",
            "audit_level": "ERROR"
        }
    ]
    '''
    if 'ref' and 'alt' in value:
        if value['ref'] == value['alt']:
            variant_id = value['@id']
            detail = f'Variant {audit_link(variant_id, variant_id)} ref and alt alleles are the same.'
            yield AuditFailure('identical alleles', detail, level='ERROR')
