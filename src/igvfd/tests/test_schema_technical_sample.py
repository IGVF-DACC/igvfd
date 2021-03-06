import pytest


def test_technical_sample_1(technical_sample_1, testapp):
    res = testapp.get(technical_sample_1['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_technical_sample_lot_id_dependency(technical_sample_1, testapp):
    res = testapp.patch_json(
        technical_sample_1['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_technical_sample_type_dependency(technical_sample_1, testapp):
    res = testapp.patch_json(
        technical_sample_1['@id'],
        {'sample_material': 'inorganic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample_1['@id'],
        {'sample_material': 'not a real type'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(technical_sample_1, testapp):
    res = testapp.patch_json(
        technical_sample_1['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample_1['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422
