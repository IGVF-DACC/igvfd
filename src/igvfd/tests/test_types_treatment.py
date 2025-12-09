import pytest


def test_treatment_summary(treatment_chemical, treatment_protein, depletion_treatment, treatment_thermal, treatment_combo1, treatment_combo2, testapp):
    res = testapp.get(treatment_chemical['@id'])
    assert res.json['summary'] == 'Treatment of 10 mM lactate for 1 hour'
    res = testapp.get(treatment_protein['@id'])
    assert res.json['summary'] == 'Treatment of 10 ng/mL G-CSF'
    res = testapp.get(depletion_treatment['@id'])
    assert res.json['summary'] == 'Depletion of penicillin for 3 minutes'
    res = testapp.get(treatment_thermal['@id'])
    assert res.json['summary'] == 'Treatment of heat exposure at 10 Celsius'
    res = testapp.get(treatment_combo1['@id'])
    assert res.json['summary'] == 'Treatment of 23 ng/mL G-CSF at 10 Celsius'
    res = testapp.get(treatment_combo2['@id'])
    print(res.json['summary'])
    assert res.json['summary'] == 'Treatment of 23 ng/mL G-CSF for 15 minutes at 10 Celsius'


def test_biosamples_treated(testapp, primary_cell_v18, treatment_v6):
    testapp.patch_json(
        primary_cell_v18['@id'],
        {
            'treatments': [treatment_v6['@id']]
        }
    )
    res = testapp.get(treatment_v6['@id'])
    assert res.json.get('biosamples_treated', []) == [primary_cell_v18['@id']]
