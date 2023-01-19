import pytest


@pytest.fixture
def measurement_set_v1(testapp, lab, award, cell_line, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sample': [cell_line['@id']],
        'donor': [human_donor['@id']]
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]
