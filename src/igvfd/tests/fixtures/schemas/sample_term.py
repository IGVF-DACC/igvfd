import pytest


@pytest.fixture
def sample_term_K562(testapp):
    item = {
        'term_id': 'EFO:0002067',
        'term_name': 'K562',
        'dbxrefs': ['Cellosaurus:CVCL_0004']
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_adrenal_gland(testapp):
    item = {
        'term_id': 'UBERON:0002369',
        'term_name': 'adrenal gland'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_1(sample_term_K562):
    item = sample_term_K562.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item
