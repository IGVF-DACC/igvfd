import pytest


def test_treatment_summary(treatment_chemical, treatment_protein, depletion_treatment, testapp):
    res = testapp.get(treatment_chemical['@id'])
    assert res.json['summary'] == 'Treatment of 10 mM lactate for 1 hour'
    res = testapp.get(treatment_protein['@id'])
    assert res.json['summary'] == 'Treatment of 10 ng/mL G-CSF'
    res = testapp.get(depletion_treatment['@id'])
    assert res.json['summary'] == 'Depletion of penicillin for 3 minutes'


def test_samples_treated(testapp, primary_cell_v18, treatment_v6):
    testapp.patch_json(
        primary_cell_v18['@id'],
        {
            'treatments': [treatment_v6['@id']]
        }
    )
    res = testapp.get(treatment_v6['@id'])
    assert res.json.get('samples_treated', []) == [primary_cell_v18['@id']]
