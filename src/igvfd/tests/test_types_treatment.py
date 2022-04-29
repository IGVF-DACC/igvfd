import pytest


def test_treatment_calculated(treatment_1, testapp):
    res = testapp.get(treatment_1['@id'])
    assert(res.json['title'] == 'Treated with 10 mM lactate for 1 hour')


def test_treatment_no_duration_calculated(treatment_2, testapp):
    res = testapp.get(treatment_2['@id'])
    assert(res.json['title'] == 'Treated with 10 ng/mL G-CSF for non-specified duration')
