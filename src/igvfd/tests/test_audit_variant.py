import pytest


def test_audit_ref_alt_check(testapp, human_genomic_variant_match):
    res = testapp.get(human_genomic_variant_match['@id'] + '@@index-data')
    print(res)
    assert any(
        error['category'] == 'variant ref and alt alleles match'
        for error in res.json['audit'].get('ERROR', [])
    )
