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
