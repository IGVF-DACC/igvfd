import pytest


@pytest.fixture
def cell_line(testapp, other_lab, award):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id']
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]
