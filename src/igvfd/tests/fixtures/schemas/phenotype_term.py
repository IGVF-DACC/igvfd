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
def phenotype_term_neuritic_plaque_measurement(testapp):
    item = {
        'term_id': 'EFO:0006798',
        'term_name': 'neuritic plaque measurement'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_mini_mental_status_exam(testapp):
    item = {
        'term_id': 'NCIT:C74982',
        'term_name': 'Mini-Mental Status Exam'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_incomplete(testapp):
    item = {
        'term_id': 'DOID:10652'
    }
    return item


@pytest.fixture
def phenotype_term_parkinsons(testapp):
    item = {
        'term_id': 'DOID:14330',
        'term_name': 'Parkinson\'s disease'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_ncit_feature(testapp):
    item = {
        'term_id': 'NCIT:C92648',
        'term_name': 'Body Weight Measurement'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_from_go(testapp):
    item = {
        'term_id': 'GO:0018214',
        'term_name': 'Protein Carboxylation'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_protein_abundance(testapp):
    item = {
        'term_id': 'NTR:0001117',
        'term_name': 'protein abundance'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_cell_growth(testapp):
    item = {
        'term_id': 'GO:0016049',
        'term_name': 'cell growth'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_cell_migration(testapp):
    item = {
        'term_id': 'GO:0016477',
        'term_name': 'cell migration'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_gene_expression(testapp):
    item = {
        'term_id': 'GO:0010467',
        'term_name': 'gene expression'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_ldl_c_uptake(testapp):
    item = {
        'term_id': 'NTR:0001118',
        'term_name': 'LDL-C uptake'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_chromatin_accessibility(testapp):
    item = {
        'term_id': 'NTR:0001119',
        'term_name': 'chromatin accessibility'
    }
    return testapp.post_json('/phenotype_term', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotype_term_v1(phenotype_term_alzheimers):
    item = phenotype_term_alzheimers.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def phenotype_term_v2(phenotype_term_v1):
    item = phenotype_term_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def phenotype_term_v4(phenotype_term_v1):
    item = phenotype_term_v1.copy()
    item.update({
        'schema_version': '4',
        'definition': 'test definition',
        'comment': 'test comment'
    })
    return item
