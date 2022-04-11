import pytest


@pytest.fixture
def tissue(testapp, lab, source, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]
