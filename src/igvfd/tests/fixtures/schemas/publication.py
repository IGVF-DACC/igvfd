import pytest


@pytest.fixture
def publication(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'title': 'Publication',
        'identifiers': ['PMID:1']
    }
    return testapp.post_json('/publication', item, status=201).json['@graph'][0]
