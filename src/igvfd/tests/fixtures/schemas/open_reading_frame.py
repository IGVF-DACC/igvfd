import pytest


def orf_foxp(testapp, gene_myc_hs):
    item = {
        'orf_id': 'CCSBORF1234',
        'geneid': 'ENSG00000185069',
        'gene': [
            gene_myc_hs['@id']
        ],
        'protein_id': 'ENSP00000001146.2',
        'dbxrefs': [
            'hORFeome:8945'
        ],
        'pct_identical_protein': 34,
        'pct_coverage_protein': 50,
        'pct_coverage_orf': 50
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]
