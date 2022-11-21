import pytest


def test_human_genomic_variant_keys(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'refseq_id': 'NC_999999.00'
    }
    response = testapp.post_json('/human_genomic_variant', item, status=201)
    assert response.status_code == 201
    response = testapp.post_json('/human_genomic_variant', item, status=409)
    assert response.status_code == 409
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'reference_sequence': 'ACTGGTCA'
    }
    response = testapp.post_json('/human_genomic_variant', item, status=201)
    assert response.status_code == 201
    response = testapp.post_json('/human_genomic_variant', item, status=409)
    assert response.status_code == 409
