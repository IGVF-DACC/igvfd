import pytest


@pytest.fixture
def tissue(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'identifiers': '2012-09-06'
    }
    return testapp.post_json('/publication', item, status=201).json['@graph'][0]
