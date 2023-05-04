import pytest


@pytest.fixture
def treatment_chemical(testapp):
    item = {
        'treatment_term_id': 'CHEBI:24996',
        'treatment_term_name': 'lactate',
        'treatment_type': 'chemical',
        'amount': 10,
        'amount_units': 'mM',
        'duration': 1,
        'duration_units': 'hour',
        'purpose': 'differentiation'
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_protein(testapp):
    item = {
        'treatment_term_id': 'UniProtKB:P09919',
        'treatment_term_name': 'G-CSF',
        'treatment_type': 'protein',
        'amount': 10,
        'amount_units': 'ng/mL',
        'purpose': 'differentiation'
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_v1(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '1',
        'documents': [],
        'aliases': []
    })
    return item


@pytest.fixture
def treatment_v2(treatment_chemical):
    item = treatment_chemical.copy()
    item.pop('purpose', None)
    item.update({
        'schema_version': '2',
        'documents': [],
        'aliases': []
    })
    return item


@pytest.fixture
def treatment_ntr(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'treatment_term_id': 'NTR:100'
    })
    return item
