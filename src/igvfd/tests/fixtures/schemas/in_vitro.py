import pytest


@pytest.fixture
def in_vitro(testapp, lab, award, source):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/in_vitro', item, status=201).json['@graph'][0]
