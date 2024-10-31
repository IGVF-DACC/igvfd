import pytest


@pytest.fixture
def model_set_no_input(
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
        'file_set_type': 'neural network',
        'prediction_objects': ['genes'],
        'software_version': software_version['@id']
    }
    return testapp.post_json('/model_set', item, status=201).json['@graph'][0]


@pytest.fixture
def model_set_v1(model_set_no_input):
    item = model_set_no_input.copy()
    item.update({
        'schema_version': '1',
        'description': ''
    })
    return item


@pytest.fixture
def model_set_v3(model_set_no_input):
    item = model_set_no_input.copy()
    item.update({
        'schema_version': '3',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def model_set_v4(model_set_no_input):
    item = model_set_no_input.copy()
    item.update({
        'schema_version': '4',
        'model_zoo_location': 'https://kipoi.org/models/Xpresso/human_K562/'
    })
    return item
