import pytest


@pytest.fixture
def publication(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'title': 'Publication',
        'identifier': ['PMID:1']
    }
    return testapp.post_json('/publication', item, status=201).json['@graph'][0]


@pytest.fixture
def publication_v1(publication):
    item = publication.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def publication_v2(publication):
    item = publication.copy()
    item.update({
        'schema_version': '2',
        'aliases': ['igvf:publication_v2'],
        'identifiers': ['doi:10.1101/2021.03.31.437978v1']
    })
    return item
