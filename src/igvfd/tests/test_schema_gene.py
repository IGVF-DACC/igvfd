import pytest


def test_gene_assembly_locations(testapp, gene_myc_hs):
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
    assert(res.status_code == 422)
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
    assert(res.status_code == 200)
