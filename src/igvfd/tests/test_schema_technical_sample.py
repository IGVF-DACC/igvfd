import pytest


def test_technical_sample(technical_sample, testapp):
    res = testapp.get(technical_sample['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_technical_sample_lot_id_dependency(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_technical_sample_type_dependency(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sample_material': 'inorganic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sample_material': 'not a real type'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_technical_sample_archived(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'status': 'archived'})
    assert res.status_code == 200
