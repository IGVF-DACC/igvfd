import pytest


def test_human_variant_keys(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'refseq_sequence_id': 'NT_999.00'
    }
    response = testapp.post_json('/human_variant', item, status=201)
    assert response.status_code == 201
    response = testapp.post_json('/human_variant', item, status=409)
    assert response.status_code == 409


def variation_type(testapp, human_variant):
    assert human_variant.json['variation_type'] == 'SNV'
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': '-',
            'alt': 'G'
        })
    assert res.json['variation_type'] == 'insertion'
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'A',
            'alt': '-'
        })
    assert res.json['variation_type'] == 'deletion'
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'A',
            'alt': 'TG'
        })
    assert res.json['variation_type'] == 'indel'
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'CGA',
            'alt': 'TG'
        })
    assert res.json['variation_type'] == 'indel'
    res = testapp.patch_json(
        human_variant['@id'],
        {
            'ref': 'CGA',
            'alt': 'GGT'
        })
    assert res.json['variation_type'] == 'MNV'
