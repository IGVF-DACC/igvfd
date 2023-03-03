import pytest


@pytest.fixture
def source(testapp):
    item = {
        'name': 'sigma',
        'title': 'Sigma-Aldrich',
        'url': 'http://www.sigmaaldrich.com'
    }
    return testapp.post_json('/source', item, status=201).json['@graph'][0]


@pytest.fixture
def other_source(testapp):
    item = {
        'description': 'American Type Culture Collection (ATCC)',
        'name': 'atcc',
        'status': 'released',
        'title': 'ATCC',
        'url': 'http://www.atcc.org/'
    }
    return testapp.post_json('/source', item, status=201).json['@graph'][0]


@pytest.fixture
def source_v1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item
