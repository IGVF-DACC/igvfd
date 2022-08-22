import pytest


def test_patch_variant(testapp, human_variant):
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'ATCG',
            'alt': 'AATCG',
            'variantid': 'rs100',
            'chromosome': 'chr2',
            'locations': [
                {
                    'assembly': 'GRCh38',
                    'position': 158180836
                }],
            'variation_type': 'insertion'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'variantid': '10041234'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'alt': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'chromosome': 'chr_2'
        }, expect_errors=True)
    assert res.status_code == 422
