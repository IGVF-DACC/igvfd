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
        audit_detail: Variant objects should have a different reference allele and alternative allele.
        audit_category: identical ref and alt alleles
        audit_levels: ERROR
    '''
    if 'ref' and 'alt' in value:
        if value['ref'] == value['alt']:
            variant_id = value['@id']
            detail = f'Variant {audit_link(variant_id, variant_id)} ref and alt alleles are the same.'
            yield AuditFailure('identical ref and alt alleles', detail, level='ERROR')
