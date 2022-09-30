import pytest


def test_patch_variant(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': '-',
            'alt': 'G',
            'rsid': 'rs100',
            'chromosome': 'chr2',
            'assembly': 'GRCh38',
            'position': 158180836
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'rsid': '10041234'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'alt': 'ABCD'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'chromosome': 'chr_2'
        }, expect_errors=True)
    assert res.status_code == 422


def test_refseq_regex(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NT_999.00'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NT_999.000'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NT_999A.00'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'MT_999A.00'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NW_999.00'
        })
    assert res.status_code == 200
