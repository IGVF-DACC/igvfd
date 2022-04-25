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
        'duration_units': 'hour',
        'uuid': 'e5db2740-c4e2-11ec-9d64-0242ac120002'
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]
