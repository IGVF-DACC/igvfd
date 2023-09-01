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
