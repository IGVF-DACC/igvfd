import pytest


@pytest.fixture
def treatment_1(testapp):
    item = {
        'treatment_term_id': 'CHEBI:24996',
        'treatment_term_name': 'lactate',
        'treatment_type': 'chemical',
        'amount': 10,
        'amount_units': 'mM',
        'duration': 1,
        'duration_units': 'hour'
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_2(testapp):
    item = {
        'treatment_term_id': 'UniProtKB:P09919',
        'treatment_term_name': 'G-CSF',
        'treatment_type': 'protein',
        'amount': 10,
        'amount_units': 'ng/mL'
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_version_v1(treatment_1):
    item = treatment_1.copy()
    item.update({
        'schema_version': '1',
        'documents': [],
        'aliases': []
    })
    return item
