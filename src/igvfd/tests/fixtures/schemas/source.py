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
def source_1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item
