import pytest


def test_summary(testapp, model_set_no_input):
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get('summary') == 'predictive model v0.0.1 neural network predicting genes'


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
