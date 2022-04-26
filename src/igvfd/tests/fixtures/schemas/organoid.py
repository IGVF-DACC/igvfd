import pytest


@pytest.fixture
def organoid(testapp, lab, award, source):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/organoid', item, status=201).json['@graph'][0]
