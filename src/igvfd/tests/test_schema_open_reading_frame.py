import pytest


def test_open_reading_frame_award_lab_requirement(testapp, award, lab, gene_myc_hs):
    item = {
        'orf_id': 'CCSBORF1234',
        'genes': [
            gene_myc_hs['@id']
        ],
    }

    res = testapp.post_json('/open_reading_frame', item, expect_errors=True)
    assert res.status_code == 422

    item = {
        'orf_id': 'CCSBORF5678',
        'genes': [
            gene_myc_hs['@id']
        ],
        'award': award['@id'],
        'lab': lab['@id']
    }

    res = testapp.post_json('/open_reading_frame', item)
    assert res.status_code == 201


def test_open_reading_frame_gene_to_genes_change(testapp, award, lab, gene_myc_hs):
    """Check for whether GENES is used as the property name instead of GENE"""
    item = {
        'orf_id': 'CCSBORF1234',
        'gene': [
            gene_myc_hs['@id']
        ],
        'award': award['@id'],
        'lab': lab['@id']
    }
    res = testapp.post_json('/open_reading_frame', item, expect_errors=True)
    assert res.status_code == 422

    item = {
        'orf_id': 'CCSBORF1234',
        'genes': [
            gene_myc_hs['@id']
        ],
        'award': award['@id'],
        'lab': lab['@id']
    }
    res = testapp.post_json('/open_reading_frame', item)
    assert res.status_code == 201
