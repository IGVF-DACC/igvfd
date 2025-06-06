import pytest


@pytest.fixture
def treatment_chemical(testapp, lab, award):
    item = {
        'treatment_term_id': 'CHEBI:24996',
        'treatment_term_name': 'lactate',
        'treatment_type': 'chemical',
        'amount': 10,
        'amount_units': 'mM',
        'duration': 1,
        'duration_units': 'hour',
        'purpose': 'differentiation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_protein(testapp, lab, award):
    item = {
        'treatment_term_id': 'UniProtKB:P09919',
        'treatment_term_name': 'G-CSF',
        'treatment_type': 'protein',
        'amount': 10,
        'amount_units': 'ng/mL',
        'purpose': 'differentiation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def depletion_treatment(testapp, lab, award):
    item = {
        'treatment_term_id': 'CHEBI:51356',
        'treatment_term_name': 'penicillin',
        'treatment_type': 'chemical',
        'duration': 3,
        'duration_units': 'minute',
        'purpose': 'selection',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': True
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
def treatment_ntr(testapp, lab, award):
    item = {
        'treatment_term_id': 'NTR:100',
        'treatment_term_name': 'interferon gamma',
        'treatment_type': 'chemical',
        'amount': 10,
        'amount_units': 'mM',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_v3(treatment_chemical):
    item = treatment_chemical.copy()
    item.pop('award', None)
    item.pop('lab', None)
    item.pop('depletion', None)
    item.update({
        'schema_version': '3',
        'documents': [],
        'aliases': []
    })
    return item


@pytest.fixture
def treatment_v4(treatment_chemical, source):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '4',
        'source': source['@id']
    })
    return item


@pytest.fixture
def treatment_v5(treatment_v4):
    item = treatment_v4.copy()
    item.update({
        'schema_version': '5',
        'description': ''
    })
    return item


@pytest.fixture
def treatment_v6(treatment_v5):
    item = treatment_v5.copy()
    item.update({
        'schema_version': '8',
        'status': 'archived'
    })
    return item


@pytest.fixture
def treatment_v7a(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '7',
        'product_id': '100A',
        'lot_id': '123'
    })
    return item


@pytest.fixture
def treatment_v7b(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '7',
        'lot_id': '123'
    })
    return item


@pytest.fixture
def treatment_v8(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '8'
    })
    return item
