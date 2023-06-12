import pytest


@pytest.fixture
def model_no_input(
    testapp,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'model_name': 'predictive model',
        'model_version': 'v0.0.1',
        'model_type': 'neural network',
        'prediction_objects': ['genes']
    }
    return testapp.post_json('/model', item, status=201).json['@graph'][0]
