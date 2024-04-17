import pytest


def test_summary(testapp, whole_organism, rodent_donor, parent_rodent_donor_1, human_donor, treatment_protein):
    res = testapp.get(whole_organism['@id'])
    assert res.json.get('summary') == 'whole organism, male, Mus musculus strain1'
    testapp.patch_json(
        whole_organism['@id'],
        {
            'lower_bound_age': 1,
            'upper_bound_age': 1,
            'age_units': 'hour'
        }
    )
    res = testapp.get(whole_organism['@id'])
    assert res.json.get('summary') == 'whole organism, male, Mus musculus strain1 (1 hour)'
    testapp.patch_json(
        whole_organism['@id'],
        {
            'donors': [rodent_donor['@id'], parent_rodent_donor_1['@id']],
            'lower_bound_age': 1,
            'upper_bound_age': 5,
            'age_units': 'hour',
            'treatments': [treatment_protein['@id']]
        }
    )
    res = testapp.get(whole_organism['@id'])
    assert res.json.get(
        'summary') == '2 whole organisms, mixed sex, Mus musculus strain1, strain2 (1-5 hours) treated with 10 ng/mL G-CSF'
