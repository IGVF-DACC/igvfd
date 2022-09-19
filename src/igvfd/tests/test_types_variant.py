import pytest


def test_human_genomic_variant_keys(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'refseq_sequence_id': 'NT_999.00'
    }
    response = testapp.post_json('/human_genomic_variant', item, status=201)
    assert response.status_code == 201
    response = testapp.post_json('/human_genomic_variant', item, status=409)
    assert response.status_code == 409


def test_variation_type(testapp, human_genomic_variant):
    assert human_genomic_variant['variation_type'] == 'SNV'
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': '-',
            'alt': 'G'
        }).json['@graph'][0]
    assert res['variation_type'] == 'insertion'
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'A',
            'alt': '-'
        }).json['@graph'][0]
    assert res['variation_type'] == 'deletion'
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'A',
            'alt': 'TG'
        }).json['@graph'][0]
    assert res['variation_type'] == 'indel'
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'CGA',
            'alt': 'TG'
        }).json['@graph'][0]
    assert res['variation_type'] == 'indel'
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'CGA',
            'alt': 'GGT'
        }).json['@graph'][0]
    assert res['variation_type'] == 'MNV'
