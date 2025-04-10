import pytest


def test_summary(testapp, model_set_no_input, gene_myc_hs, gene_CRLF2_par_y, gene_CD1E, gene_TAB3_AS1, gene_MAGOH2P, gene_zscan10_mm):
    # Test Model Set summary if without assessed genes
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get('summary') == 'predictive model v0.0.1 neural network predicting genes'

    # Test Model Set summary if with 5 assessed genes
    testapp.patch_json(
        model_set_no_input['@id'],
        {
            'assessed_genes':
                [gene_myc_hs['@id'],
                 gene_CRLF2_par_y['@id'],
                 gene_CD1E['@id'],
                 gene_TAB3_AS1['@id'],
                 gene_MAGOH2P['@id']
                 ]
        }
    )
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get(
        'summary') == 'predictive model v0.0.1 neural network for CD1E, CRLF2, MAGOH2P, MYC, TAB3-AS1 predicting genes'

    # Test Model Set summary if with 6+ assessed gene
    testapp.patch_json(
        model_set_no_input['@id'],
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
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get(
        'summary') == 'predictive model v0.0.1 neural network for 6 assessed genes predicting genes'


def test_calculated_externally_hosted(testapp, model_file, model_set_no_input):
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get('externally_hosted') == False
    testapp.patch_json(
        model_file['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'https://tested_url',
            'file_set': model_set_no_input['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get('externally_hosted') == True


def test_software_versions(testapp, model_file, model_set_no_input, analysis_step_version, software_version):
    res = testapp.get(model_set_no_input['@id'])
    testapp.patch_json(
        model_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id'],
            'file_set': model_set_no_input['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'])
    assert set([software_version_object['@id']
               for software_version_object in res.json.get('software_versions')]) == {software_version['@id']}
