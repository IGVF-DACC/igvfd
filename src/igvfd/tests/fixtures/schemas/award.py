import pytest


@pytest.fixture
def award(testapp):
    item = {
        'name': 'igvf-award',
        'project': 'IGVF',
        'title': 'A Generic IGVF Award',
        'viewing_group': 'IGVF',
    }
    return testapp.post_json('/award', item).json['@graph'][0]


@pytest.fixture
def award_1(award):
    item = award.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item
