import pytest


@pytest.fixture
def treatment(testapp, treatment_term_id, treatment_term_name, amount, duration):
    item = {
        'treatment_term_id': 'CHEBI:24996',
        'treatment_term_name': 'lactate',
        'amount': 10,
        'amount_units': 'mM',
        'duration': 1,
        'duration_units': 'hour',
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]
