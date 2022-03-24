import pytest


def test_sample_1(sample_1, testapp):
    res = testapp.get(sample_1['@id'])
    assert(res.json['accession'][:6] == "IGVFSM")


def test_lot_id_dependency(sample_1, testapp):
    res = testapp.patch_json(
        sample_1['@id'],
        {"lot_id": "R00002"}, expect_errors=True)
    assert(res.status_code == 422)
