import pytest


def test_treatment_calculated(treatment_chemical, testapp):
    res = testapp.get(treatment_chemical['@id'])
    assert res.json['title'] == 'Treatment of 10 mM lactate for 1 hour'


def test_treatment_no_duration_calculated(treatment_protein, testapp):
    res = testapp.get(treatment_protein['@id'])
    assert res.json['title'] == 'Treatment of 10 ng/mL G-CSF'
