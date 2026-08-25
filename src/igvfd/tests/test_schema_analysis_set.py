import pytest


def test_file_set_type_dependency(analysis_set_base, measurement_set, testapp):
    res = testapp.patch_json(
        analysis_set_base['@id'],
        {'file_set_type': 'principal analysis'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        analysis_set_base['@id'],
        {'file_set_type': 'principal analysis',
         'input_file_sets': [measurement_set['@id']]})
    assert res.status_code == 200


def test_condition_treatments(
    testapp,
    analysis_set_base,
    measurement_set,
    primary_cell,
    treatment_combo1,
    treatment_combo2,
):
    testapp.patch_json(
        primary_cell['@id'],
        {
            'treatments': [treatment_combo1['@id'], treatment_combo2['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']],
            'condition_treatments': [treatment_combo1['@id'], treatment_combo2['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    condition_treatment_ids = {
        treatment if isinstance(treatment, str) else treatment['@id']
        for treatment in res.json['condition_treatments']
    }
    assert condition_treatment_ids == {
        treatment_combo1['@id'],
        treatment_combo2['@id'],
    }
    assert 'perturbed with 23 ng/mL G-CSF at 10 Celsius' in res.json['sample_summary']


def test_condition_treatments_differential_sample_summary(
    testapp,
    analysis_set_base,
    measurement_set,
    primary_cell,
    in_vitro_cell_line,
    lab,
    award,
):
    treatment_8mM_glucose = testapp.post_json('/treatment', {
        'treatment_term_id': 'CHEBI:17234',
        'treatment_term_name': 'glucose',
        'treatment_type': 'chemical',
        'amount': 8,
        'amount_units': 'mM',
        'duration': 72,
        'duration_units': 'hour',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False,
    }, status=201).json['@graph'][0]
    treatment_33mM_glucose = testapp.post_json('/treatment', {
        'treatment_term_id': 'CHEBI:17234',
        'treatment_term_name': 'glucose',
        'treatment_type': 'chemical',
        'amount': 33,
        'amount_units': 'mM',
        'duration': 72,
        'duration_units': 'hour',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False,
    }, status=201).json['@graph'][0]
    treatment_bsa = testapp.post_json('/treatment', {
        'treatment_term_id': 'CHEBI:27583',
        'treatment_term_name': 'BSA',
        'treatment_type': 'chemical',
        'amount': 1,
        'amount_units': 'mM',
        'duration': 72,
        'duration_units': 'hour',
        'purpose': 'control',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False,
    }, status=201).json['@graph'][0]
    treatment_palmitate = testapp.post_json('/treatment', {
        'treatment_term_id': 'CHEBI:15756',
        'treatment_term_name': 'palmitate',
        'treatment_type': 'chemical',
        'amount': 1,
        'amount_units': 'mM',
        'duration': 72,
        'duration_units': 'hour',
        'purpose': 'perturbation',
        'award': award['@id'],
        'lab': lab['@id'],
        'depletion': False,
    }, status=201).json['@graph'][0]

    testapp.patch_json(
        primary_cell['@id'],
        {
            'treatments': [
                treatment_33mM_glucose['@id'],
                treatment_bsa['@id'],
                treatment_palmitate['@id'],
            ]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'treatments': [
                treatment_8mM_glucose['@id'],
                treatment_bsa['@id'],
            ]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']],
            'condition_treatments': [
                treatment_33mM_glucose['@id'],
                treatment_bsa['@id'],
                treatment_palmitate['@id'],
                treatment_8mM_glucose['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert '33 mM glucose, 1 mM palmitate vs. 8 mM glucose' in res.json['sample_summary']
