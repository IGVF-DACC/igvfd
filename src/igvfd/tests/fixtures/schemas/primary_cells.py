import pytest


@pytest.fixture
def primary_cells(testapp, other_lab, award):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id']
    }
    return testapp.post_json('/primary_cells', item, status=201).json['@graph'][0]
