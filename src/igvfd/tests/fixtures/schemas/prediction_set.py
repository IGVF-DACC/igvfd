import pytest


@pytest.fixture
def base_prediction_set(testapp, lab, award, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'pathogenicity',
        'samples': [in_vitro_cell_line['@id']]
    }
    return testapp.post_json('/prediction_set', item).json['@graph'][0]


@pytest.fixture
def prediction_set_functional_effect(testapp, lab, award, multiplexed_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'functional effect',
        'samples': [multiplexed_sample['@id']]
    }
    return testapp.post_json('/prediction_set', item).json['@graph'][0]


@pytest.fixture
def prediction_set_v1(base_prediction_set):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def prediction_set_v2(prediction_set_v1):
    item = prediction_set_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
