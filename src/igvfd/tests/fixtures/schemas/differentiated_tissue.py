import pytest


@pytest.fixture
def differentiated_tissue(testapp, lab, award, source):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
    return testapp.post_json('/differentiated_tissue', item, status=201).json['@graph'][0]
