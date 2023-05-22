import pytest


def test_audit_ref_alt_check(testapp, human_genomic_variant_match):
    res = testapp.get(human_genomic_variant_match['@id'] + '@@index-data')
    assert any(
        error['category'] == 'identical ref and alt alleles'
        for error in res.json['audit'].get('ERROR', [])
    )
