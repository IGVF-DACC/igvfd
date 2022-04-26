import pytest


@pytest.fixture
def assay_ontology_term_1(testapp):
    item = {
        'term_id': 'OBI:0002041',
        'term_name': 'STARR-seq'
    }
    return testapp.post_json('/assay_ontology_term', item, status=201).json['@graph'][0]