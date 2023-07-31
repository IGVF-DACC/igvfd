import pytest


@pytest.fixture
def model_no_input(
    testapp,
    award,
    lab,
    software_version
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'model_name': 'predictive model',
        'model_version': 'v0.0.1',
        'model_type': 'neural network',
        'prediction_objects': ['genes'],
        'software_version': software_version['@id']
    }
    return testapp.post_json('/model', item, status=201).json['@graph'][0]


@pytest.fixture
def model_v1(model_no_input):
    item = model_no_input.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item
