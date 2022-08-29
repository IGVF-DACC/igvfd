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
def sample_term_pluripotent_stem_cell(testapp):
    item = {
        'term_id': 'CL:0002248',
        'term_name': 'pluripotent stem cell'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_whole_organism(testapp):
    item = {
        'term_id': 'UBERON:0000468',
        'term_name': 'whole organism'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_v1(sample_term_K562):
    item = sample_term_K562.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def sample_term_technical_sample(testapp):
    item = {
        'term_id': 'NTR:0000637',
        'term_name': 'technical sample'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]
