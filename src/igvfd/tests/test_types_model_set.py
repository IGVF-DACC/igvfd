import pytest


def test_summary(testapp, model_set_no_input):
    res = testapp.get(model_set_no_input['@id'])
    assert res.json.get('summary') == 'predictive model v0.0.1 neural network predicting genes'
