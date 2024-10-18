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
