import pytest


@pytest.fixture
def base_prediction(testapp, lab, award, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'pathogenicity',
        'samples': [in_vitro_cell_line['@id']]
    }
    return testapp.post_json('/prediction', item).json['@graph'][0]


@pytest.fixture
def prediction_v1(base_prediction):
    item = base_prediction.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def prediction_v2(
    lab,
    award,
    in_vitro_cell_line
):
    item = {
        'schema_version': '2',
        'award': award['@id'],
        'lab': lab['@id'],
        'prediction_type': 'pathogenicity',
        'samples': [in_vitro_cell_line['@id']]
    }
    return item
