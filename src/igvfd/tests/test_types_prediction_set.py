import pytest


def test_summary(testapp, base_prediction_set, prediction_set_donor, gene_myc_hs, gene_CRLF2_par_y, gene_CD1E, gene_TAB3_AS1, gene_MAGOH2P, gene_zscan10_mm, tabular_file, analysis_step_version, in_vitro_organoid, in_vitro_cell_line, tissue, whole_organism):
    # Test Prediction Set summary if without assessed genes
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'functional effect prediction in Mus musculus strain1 (male) K562 cell line'

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
        'summary') == 'functional effect prediction for CD1E, CRLF2, MAGOH2P, MYC, TAB3-AS1 using Bowtie2 v2.4.4 in Mus musculus strain1 (male) K562 cell line'

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
    assert res.json.get(
        'summary') == 'functional effect prediction for 6 assessed genes using Bowtie2 v2.4.4 in Mus musculus strain1 (male) K562 cell line'

    # Test Prediction Set summary if with 2 samples, listing out samples in summary
    testapp.patch_json(
        base_prediction_set['@id'],
        {
            'samples':
                [
                    in_vitro_cell_line['@id'],
                    in_vitro_organoid['@id']
                ]
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get('summary') == 'functional effect prediction for 6 assessed genes using Bowtie2 v2.4.4 in Mus musculus strain1 (male) K562 cell line, Homo sapiens adrenal gland organoid induced to adrenal gland for 10 days'

    # Test Prediction Set summary if with 3+ samples, use sample number instead
    testapp.patch_json(
        base_prediction_set['@id'],
        {
            'samples':
                [
                    in_vitro_cell_line['@id'],
                    in_vitro_organoid['@id'],
                    tissue['@id'],
                    whole_organism['@id']
                ]
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert res.json.get(
        'summary') == 'functional effect prediction for 6 assessed genes using Bowtie2 v2.4.4 in 4 mixed species samples'

    # Test Prediction Set summary if donors specified instead of samples
    res = testapp.get(prediction_set_donor['@id'])
    assert res.json.get('summary') == 'functional effect prediction in Homo sapiens'


def test_software_versions(testapp, tabular_file, base_prediction_set, analysis_step_version, software_version):
    res = testapp.get(base_prediction_set['@id'])
    testapp.patch_json(
        tabular_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id'],
            'file_set': base_prediction_set['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'])
    assert set([software_version_object['@id']
               for software_version_object in res.json.get('software_versions')]) == {software_version['@id']}
