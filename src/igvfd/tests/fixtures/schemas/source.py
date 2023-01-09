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
def source_v1(source):
    item = source.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def source_v2(source):
    item = source.copy()
    item.update({
        'schema_version': '2',
        'aliases': ['igvf:source_v2']
    })
    return item
