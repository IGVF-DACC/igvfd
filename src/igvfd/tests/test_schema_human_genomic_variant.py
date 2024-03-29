import pytest


def test_post_variant(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000
    }
    response = testapp.post_json('/human_genomic_variant', item, expect_errors=True)
    assert response.status_code == 422
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'refseq_id': 'NC_000001.5'
    }
    response = testapp.post_json('/human_genomic_variant', item)
    assert response.status_code == 201
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'reference_sequence': 'ACTG'
    }
    response = testapp.post_json('/human_genomic_variant', item)
    assert response.status_code == 201
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'refseq_id': 'NC_000001.5',
        'reference_sequence': 'ACTG'
    }
    response = testapp.post_json('/human_genomic_variant', item, expect_errors=True)
    assert response.status_code == 422


def test_patch_variant(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'ref': 'C',
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


def test_rsid_regex(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'rsid': 'rs1123553qwe'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'rsid': 'rs645731345xrqw123'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'rsid': 'rs123456789'
        })
    assert res.status_code == 200


def test_associated_gwas_regex(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'associated_gwas': ['GCST90019034a']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'associated_gwas': ['GCST90X31t0052']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'associated_gwas': ['GCST6405606023']
        })
    assert res.status_code == 200


def test_refseq_regex(testapp, human_genomic_variant):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_123456.00'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_123456.000'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_12345A.00'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_1234567.00'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NT_123456.00'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_654321.09'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {
            'refseq_id': 'NC_654321x08'
        }, expect_errors=True)
    assert res.status_code == 422


def test_refseq_id_reference_sequence_dependency(
    testapp,
    human_genomic_variant,
    human_genomic_variant_no_refseq_id
):
    res = testapp.patch_json(
        human_genomic_variant['@id'],
        {'reference_sequence': 'ACTGGAA'},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        human_genomic_variant_no_refseq_id['@id'],
        {'refseq_id': 'NC_666666.1'},
        expect_errors=True
    )
    assert res.status_code == 422
