import pytest


@pytest.fixture
def sample_ontology_term_1(testapp):
    item = {
        'term_id': 'EFO:0002067',
        'term_name': 'K562',
        'dbxrefs': ['Cellosaurus:CVCL_0004']
    }
    return testapp.post_json('/sample_ontology_term', item, status=201).json['@graph'][0]
