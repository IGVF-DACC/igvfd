import pytest


def test_sample_1(human_donor, testapp):
    res = testapp.get(human_donor['@id'])
    assert(res.json['accession'][:6] == 'IGVFDO')


def test_health_status_dependency(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)


def test_ethnicity_dependency(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicity': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)
