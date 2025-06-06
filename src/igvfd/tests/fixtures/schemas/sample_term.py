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
        'term_name': 'whole organism',
        'uuid': '25d5ad53-15fd-4a44-878a-ece2f7e86509'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_endothelial_cell(testapp):
    item = {
        'term_id': 'CL:0002139',
        'term_name': 'endothelial cell of vascular tree'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_embryoid_body(testapp):
    item = {
        'term_id': 'NTR:0000428',
        'term_name': 'embryoid body'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_gastrula(testapp):
    item = {
        'term_id': 'UBERON:0004734',
        'term_name': 'gastrula'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_brown_adipose_tissue(testapp):
    item = {
        'term_id': 'UBERON:0001348',
        'term_name': 'brown adipose tissue'
    }
    return testapp.post_json('/sample_term', item, status=201).json['@graph'][0]


@pytest.fixture
def sample_term_lymphoblastoid(testapp):
    item = {
        'term_id': 'EFO:0005292',
        'term_name': 'lymphoblastoid cell line'
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


@pytest.fixture
def sample_term_v2(sample_term_v1):
    item = sample_term_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def sample_term_v4(sample_term_v1):
    item = sample_term_v1.copy()
    item.update({
        'schema_version': '4',
        'dbxrefs': []
    })
    return item


@pytest.fixture
def sample_term_v5(sample_term_v1):
    item = sample_term_v1.copy()
    item.update({
        'schema_version': '5',
        'definition': 'test definition',
        'comment': 'test comment'
    })
    return item
