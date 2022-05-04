import pytest


@pytest.fixture
def assay_ontology_term_starr(testapp):
    item = {
        'term_id': 'OBI:0002041',
        'term_name': 'STARR-seq'
    }
    return testapp.post_json('/assay_ontology_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_ontology_term_chip(testapp):
    item = {
        'term_id': 'OBI:0000716',
        'term_name': 'ChIP-seq'
    }
    return testapp.post_json('/assay_ontology_term', item, status=201).json['@graph'][0]
