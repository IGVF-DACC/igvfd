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
def assay_term_v1(assay_term_starr):
    item = assay_term_starr.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def assay_term_v2(assay_term_starr):
    item = assay_term_starr.copy()
    item.update({
        'schema_version': '2',
        'aliases': ['igvf:assay_term_v2'],
        'deprecated_ntr_terms': ['NTR:0000009']
    })
    return item
