import pytest


@pytest.fixture
def organism1(testapp, lab, source, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/organism', item, status=201).json['@graph'][0]
