import pytest


def test_human_variant_keys(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100'
    }
    response = testapp.post_json('/human_variant', item, status=201)
    assert response.status_code == 201
    response = testapp.post_json('/human_variant', item, status=409)
    assert response.status_code == 409
