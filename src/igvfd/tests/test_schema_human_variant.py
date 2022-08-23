import pytest


def test_patch_variant(testapp, human_variant):
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'ATCG',
            'alt': 'AATCG',
            'rsid': 'rs100',
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
            'rsid': '10041234'
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


def test_dbxrefs_regex(testapp, human_variant):
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'dbxrefs': ['X-999999-GTCA-CG', '999'],
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'dbxrefs': ['X-999999-GTCA', 'AAAA'],
        }, expect_errors=True)
    assert res.status_code == 422
