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
    '''Variant object reference allele and alternative allele should never be the same, if they are they should trigger an ERROR.'''
    if 'ref' and 'alt' in value:
        if value['ref'] == value['alt']:
            variant_id = value['@id']
            detail = f'Variant {audit_link(variant_id, variant_id)} ref and alt alleles are the same.'
            yield AuditFailure('variant ref and alt alleles match', detail, level='ERROR')
