import pytest


@pytest.fixture
def phenotype_term_alzheimers(testapp):
    item = {
        'term_id': 'DOID:10652',
        'term_name': 'Alzheimer\'s disease'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_myocardial_infarction(testapp):
    item = {
        'term_id': 'HP:0001658',
        'term_name': 'Myocardial infarction'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_incomplete(testapp):
    item = {
        'term_id': 'DOID:10652'
    }
    return item


@pytest.fixture
def phenotype_term_v1(phenotype_term_alzheimers):
    item = phenotype_term_alzheimers.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def phenotype_term_ncit_feature(testapp):
    item = {
        'term_id': 'NCIT:C92648',
        'term_name': 'Body Weight Measurement'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_v2(phenotype_term_v1):
    item = phenotype_term_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def phenotype_term_from_go(testapp):
    item = {
        'term_id': 'GO:0018214',
        'term_name': 'Protein Carboxylation'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]
