import pytest


def test_gene_assembly_locations_hs(testapp, gene_myc_hs):
    res = testapp.patch_json(
        gene_myc_hs['@id'],
        {
            'locations': [
                {
                    'assembly': 'mm10',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        gene_myc_hs['@id'],
        {
            'locations': [
                {
                    'assembly': 'mm9',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        gene_myc_hs['@id'],
        {
            'locations': [
                {
                    'assembly': 'GRCm39',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        gene_myc_hs['@id'],
        {
            'locations': [
                {
                    'assembly': 'hg19',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        gene_myc_hs['@id'],
        {
            'locations': [
                {
                    'assembly': 'GRCh38',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }
    )
    assert res.status_code == 200


def test_gene_assembly_locations_mm(testapp, gene_zscan10_mm):
    res = testapp.patch_json(
        gene_zscan10_mm['@id'],
        {
            'locations': [
                {
                    'assembly': 'hg19',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        gene_zscan10_mm['@id'],
        {
            'locations': [
                {
                    'assembly': 'GRCh38',
                    'chromosome': 'chr18',
                    'start': 47808713,
                    'end': 47814692
                }
            ]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        gene_zscan10_mm['@id'],
        {
            'locations': [
                {
                    'assembly': 'mm9',
                    'chromosome': 'chr17',
                    'start': 23737823,
                    'end': 23747986
                }
            ]
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        gene_zscan10_mm['@id'],
        {
            'locations': [
                {
                    'assembly': 'mm10',
                    'chromosome': 'chr17',
                    'start': 23600826,
                    'end': 23611019
                }
            ]
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        gene_zscan10_mm['@id'],
        {
            'locations': [
                {
                    'assembly': 'GRCm39',
                    'chromosome': 'chr17',
                    'start': 23819830,
                    'end': 23829993
                }
            ]
        }
    )
    assert res.status_code == 200
