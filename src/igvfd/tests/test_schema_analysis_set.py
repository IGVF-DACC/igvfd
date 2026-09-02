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
    assert 'perturbed with 23 ng/mL G-CSF at 10 Celsius' in res.json['simplified_sample_summary']


def test_condition_treatments_differential_sample_summary(
    testapp,
    analysis_set_base,
    measurement_set_mpra,
    measurement_set_multiome_2,
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
        analysis_set_base['@id'],
        {
            'input_file_sets': [
                measurement_set_mpra['@id'],
                measurement_set_multiome_2['@id'],
            ],
            'condition_treatments': [
                treatment_33mM_glucose['@id'],
                treatment_bsa['@id'],
                treatment_palmitate['@id'],
                treatment_8mM_glucose['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json['simplified_sample_summary'].endswith(
        'under conditions of 33 mM glucose, 1 mM palmitate and 8 mM glucose'
    )


def test_condition_treatments_differential_sample_summary_many_conditions(
    testapp,
    analysis_set_base,
    measurement_set,
    measurement_set_mpra,
    measurement_set_multiome_2,
    primary_cell,
    in_vitro_cell_line,
    tissue,
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
        {'treatments': [treatment_33mM_glucose['@id'], treatment_palmitate['@id']]}
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'treatments': [treatment_8mM_glucose['@id']]}
    )
    testapp.patch_json(
        tissue['@id'],
        {'treatments': [treatment_33mM_glucose['@id']]}
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [
                measurement_set_mpra['@id'],
                measurement_set_multiome_2['@id'],
                measurement_set['@id'],
            ],
            'condition_treatments': [
                treatment_33mM_glucose['@id'],
                treatment_palmitate['@id'],
                treatment_8mM_glucose['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json['simplified_sample_summary'].endswith(
        'under conditions of 33 mM glucose, 1 mM palmitate and 2 more'
    )


def test_condition_treatments_multiplexed_sample_summary(
    testapp,
    analysis_set_base,
    measurement_set,
    multiplexed_sample,
    tissue,
    in_vitro_cell_line,
    post_chemical_treatment,
):
    treatment_glucose = post_chemical_treatment('glucose', 'CHEBI:17234', 8)
    treatment_palmitate = post_chemical_treatment('palmitate', 'CHEBI:15756', 1)
    testapp.patch_json(tissue['@id'], {'treatments': [treatment_glucose['@id']]})
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'treatments': [treatment_palmitate['@id']]}
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'samples': [multiplexed_sample['@id']]}
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']],
            'condition_treatments': [
                treatment_glucose['@id'],
                treatment_palmitate['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json['simplified_sample_summary'].endswith(
        'under conditions of 1 mM palmitate and 8 mM glucose'
    )


def test_condition_treatments_unique_labels(
    testapp,
    analysis_set_base,
    measurement_set,
    measurement_set_mpra,
    primary_cell,
    tissue,
    post_chemical_treatment,
):
    leucine_24h = post_chemical_treatment('leucine', 'CHEBI:15603', 10, duration=24)
    leucine_6h = post_chemical_treatment('leucine', 'CHEBI:15603', 10, duration=6)
    lps = post_chemical_treatment('lipopolysaccharide', 'CHEBI:16412', 1)
    testapp.patch_json(
        primary_cell['@id'],
        {'treatments': [leucine_24h['@id'], leucine_6h['@id']]}
    )
    testapp.patch_json(
        tissue['@id'],
        {'treatments': [lps['@id']]}
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [
                measurement_set_mpra['@id'],
                measurement_set['@id'],
            ],
            'condition_treatments': [
                leucine_24h['@id'],
                leucine_6h['@id'],
                lps['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    summary = res.json['simplified_sample_summary']
    assert '10 mM leucine, 10 mM leucine' not in summary
    assert summary.endswith(
        'under conditions of 1 mM lipopolysaccharide and 10 mM leucine'
    )
