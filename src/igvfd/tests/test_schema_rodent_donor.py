import pytest


def test_sample_1(rodent_donor, testapp):
    res = testapp.get(rodent_donor['@id'])
    assert(res.json['accession'][:6] == 'IGVFDO')


def test_lot_id_dependency(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)
