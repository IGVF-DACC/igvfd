import pytest


def test_summary(testapp, base_prediction_set, gene_myc_hs, gene_CRLF2_par_y, gene_CD1E, gene_TAB3_AS1, gene_MAGOH2P, gene_zscan10_mm, tabular_file, analysis_step_version):
    # Test Prediction Set summary if without assessed genes
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'functional effect prediction'

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
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get(
        'summary') == 'functional effect prediction for CD1E, CRLF2, MAGOH2P, MYC, TAB3-AS1 using Bowtie2 v2.4.4'

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
    assert res.json.get('summary') == 'functional effect prediction for 6 assessed genes using Bowtie2 v2.4.4'
