import pytest


@pytest.fixture
def differentiated_cell(testapp, lab, award, source):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/differentiated_cell', item, status=201).json['@graph'][0]
