import pytest


@pytest.fixture
def whole_organism1(testapp, lab, source, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]
