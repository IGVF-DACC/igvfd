import pytest


@pytest.fixture
def award(testapp):
    item = {
        'name': 'igvf-award',
        'rfa': 'IGVF',
        'project': 'IGVF',
        'title': 'A Generic IGVF Award',
        'viewing_group': 'IGVF',
    }
    return testapp.post_json('/award', item).json['@graph'][0]
