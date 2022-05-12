import pytest


@pytest.fixture
def trait_ontology_term_epilepsy(testapp):
    item = {
        'term_id': 'MONDO:0005027',
        'term_name': 'epilepsy'
    }
    return testapp.post_json('/trait_ontology_term', item, status=201).json['@graph'][0]


@pytest.fixture
def trait_ontology_term_cell_size(testapp):
    item = {
        'term_id': 'OBA:0000055',
        'term_name': 'cell size'
    }
    return testapp.post_json('/trait_ontology_term', item, status=201).json['@graph'][0]
