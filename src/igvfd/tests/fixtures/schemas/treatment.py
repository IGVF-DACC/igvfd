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

<<<<<<< HEAD
@pytest.fixture
=======

<<<<<<< HEAD
>>>>>>> 950b9e5 (update required)
=======
@pytest.fixture
>>>>>>> 97e30e7 (update tests)
def treatment_2(testapp):
    item = {
        'treatment_term_id': 'UniProtKB:P09919',
        'treatment_term_name': 'G-CSF',
        'treatment_type': 'protein',
        'amount': 10,
<<<<<<< HEAD
<<<<<<< HEAD
        'amount_units': 'ng/mL'
=======
        'amount_units': 'ng/kg'
>>>>>>> 950b9e5 (update required)
=======
        'amount_units': 'ng/mL'
>>>>>>> 97e30e7 (update tests)
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]
