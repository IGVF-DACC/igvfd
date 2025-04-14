import pytest


def test_summary(testapp, base_prediction_set, gene_myc_hs, gene_CRLF2_par_y, gene_CD1E, gene_TAB3_AS1, gene_MAGOH2P, gene_zscan10_mm):
    # Test Prediction Set summary if without assessed genes
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'pathogenicity prediction'

    # Test Prediction Set summary if with assessed genes
    testapp.patch_json(
        base_prediction_set['@id'],
        {
            'assessed_genes':
                [
                    gene_myc_hs['@id'],
                    gene_CRLF2_par_y['@id'],
                    gene_CD1E['@id'],
                    gene_TAB3_AS1['@id'],
                    gene_MAGOH2P['@id']
                ]
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'pathogenicity prediction for CD1E, CRLF2, MAGOH2P, MYC, TAB3-AS1'

    # Test Prediction Set summary if with 6+ assessed genes
    testapp.patch_json(
        base_prediction_set['@id'],
        {
            'assessed_genes':
                [
                    gene_myc_hs['@id'],
                    gene_CRLF2_par_y['@id'],
                    gene_CD1E['@id'],
                    gene_TAB3_AS1['@id'],
                    gene_MAGOH2P['@id'],
                    gene_zscan10_mm['@id']
                ]
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'pathogenicity prediction for 6 assessed genes'
