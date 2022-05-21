import pytest


def test_sample_1(primary_cell, testapp):
    res = testapp.get(primary_cell['@id'])
    assert(res.json['accession'][:6] == 'IGVFSM')


def test_lot_id_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)


def test_age_unit_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'organism': 'Homo sapiens', 'age': '5', 'age_units': 'year'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'organism': 'Saccharomyces', 'age_units': 'year'}, expect_errors=True)
    assert(res.status_code == 422)


def test_lifestage_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'organism': 'Homo sapiens', 'life_stage': 'adult'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'organism': 'Mus musculus', 'life_stage': 'stationary'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'organism': 'Saccharomyces', 'life_stage': 'adult'}, expect_errors=True)
    assert(res.status_code == 422)


def test_nih_institutional_certification(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'nih_institutional_certification': 'NICHD1455'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'nih_institutional_certification': 'ABBBCCCHD1455'}, expect_errors=True)
    assert(res.status_code == 422)


def test_collections(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collections': ['ENCODE']})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert(res.status_code == 422)
