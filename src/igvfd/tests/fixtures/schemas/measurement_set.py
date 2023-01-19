import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_v1(measurement_set, cell_line, human_donor):
    item = measurement_set.copy()
    item.update({
        'schema_version': '1',
        'sample': [cell_line['@id']],
        'donor': [human_donor['@id']]
    })
    return item
