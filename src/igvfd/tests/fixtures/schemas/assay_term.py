import pytest


@pytest.fixture
def assay_term_starr(testapp):
    item = {
        'term_id': 'OBI:0002041',
        'term_name': 'STARR-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_chip(testapp):
    item = {
        'term_id': 'OBI:0000716',
        'term_name': 'ChIP-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_dnase(testapp):
    item = {
        'term_id': 'OBI:0001853',
        'term_name': 'DNase-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_atac(testapp):
    item = {
        'term_id': 'OBI:002039',
        'term_name': 'ATAC-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_rna(testapp):
    item = {
        'term_id': 'OBI:0001271',
        'term_name': 'RNA-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_v1(assay_term_starr):
    item = assay_term_starr.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def assay_term_ntr(testapp):
    item = {
        'term_id': 'NTR:00001',
        'term_name': 'example-tn-1'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_mpra(testapp):
    item = {
        'term_id': 'OBI:0002675',
        'term_name': 'massively parallel reporter assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_crispr(testapp):
    item = {
        'term_id': 'NTR:0000520',
        'term_name': 'CRISPR screen'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_v2(assay_term_v1):
    item = assay_term_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
