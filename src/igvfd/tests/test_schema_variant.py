import pytest


def test_patch_variant(testapp, variant):
    res = testapp.patch_json(
        variant['@id'],
        {
            'ref': 'ATCG',
            'alt': 'AATCG',
            'variantid': 'rs100',
            'locations': [
                {
                    'assembly': 'mm10',
                    'chromosome': 'chr2',
                    'position': 158180836
                }],
            'variation_type': 'insertion'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        variant['@id'],
        {
            'variantid': '10041234'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        variant['@id'],
        {
            'ref': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        variant['@id'],
        {
            'alt': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        variant['@id'],
        {
            'locations': [{
                'chromosome': 'chr_2'
            }]
        }, expect_errors=True)
    assert res.status_code == 422
