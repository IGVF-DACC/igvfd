import pytest


@pytest.fixture
def disease_ontology_term_alzheimers(testapp):
    item = {
        'term_id': 'DOID:10652',
        'term_name': 'Alzheimer\'s disease'
    }
    return testapp.post_json('/disease_ontology_term', item, status=201).json['@graph'][0]


@pytest.fixture
def disease_ontology_term_myocardial_infarction(testapp):
    item = {
        'term_id': 'HP:0001658',
        'term_name': 'Myocardial infarction'
    }
    return testapp.post_json('/disease_ontology_term', item, status=201).json['@graph'][0]
