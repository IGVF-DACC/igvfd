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
        'purpose': 'activation',
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
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_thermal(testapp, lab, award):
    """Treatment with temperature only (no amount); uses chemical type."""
    item = {
        'treatment_term_id': 'NTR:9919',
        'treatment_term_name': 'heat exposure',
        'treatment_type': 'chemical',
        'temperature': 10,
        'temperature_units': 'Celsius',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_diet(testapp, lab, award):
    item = {
        'treatment_term_id': 'NCIT:C15222',
        'treatment_term_name': 'High Fat Diet',
        'treatment_type': 'diet',
        'duration': 84,
        'duration_units': 'day',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_diet_no_duration(testapp, lab, award):
    item = {
        'treatment_term_id': 'NCIT:C15222',
        'treatment_term_name': 'High Fat Diet',
        'treatment_type': 'diet',
        'purpose': 'control',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_normal_diet(testapp, lab, award):
    item = {
        'treatment_term_id': 'NCIT:C15222',
        'treatment_term_name': 'Normal Diet',
        'treatment_type': 'diet',
        'duration': 84,
        'duration_units': 'day',
        'purpose': 'control',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_combo1(testapp, lab, award):
    item = {
        'treatment_term_id': 'NTR:9919',
        'treatment_term_name': 'G-CSF',
        'amount': 23,
        'amount_units': 'ng/mL',
        'treatment_type': 'chemical',
        'temperature': 10,
        'temperature_units': 'Celsius',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False
    }
    return testapp.post_json('/treatment', item, status=201).json['@graph'][0]


@pytest.fixture
def treatment_combo2(testapp, lab, award):
    item = {
        'treatment_term_id': 'NTR:9919',
        'treatment_term_name': 'G-CSF',
        'amount': 23,
        'amount_units': 'ng/mL',
        'duration': 15,
        'duration_units': 'minute',
        'treatment_type': 'chemical',
        'temperature': 10,
        'temperature_units': 'Celsius',
        'purpose': 'perturbation',
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


@pytest.fixture
def treatment_v9(treatment_chemical):
    item = treatment_chemical.copy()
    item.update({
        'schema_version': '9',
        'treatment_type': 'environmental'
    })
    return item


@pytest.fixture
def treatment_v10_thermal(treatment_thermal):
    """Treatment with schema_version 10 and treatment_type thermal for upgrade testing."""
    item = treatment_thermal.copy()
    item['schema_version'] = '10'
    item['treatment_type'] = 'thermal'
    return item


@pytest.fixture
def treatment_v11(lab, award):
    return {
        'treatment_term_id': 'NTR:0001001',
        'treatment_term_name': 'High Fat Diet',
        'treatment_type': 'diet',
        'duration': 84,
        'duration_units': 'day',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False,
        'schema_version': '11',
    }
