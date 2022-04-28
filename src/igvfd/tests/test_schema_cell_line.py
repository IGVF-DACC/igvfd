import pytest


def test_sample_1(cell_line, testapp):
    res = testapp.get(cell_line['@id'])
    assert(res.json['accession'][:6] == 'IGVFSM')


def test_lot_id_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)


def test_age_unit_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'organism': 'Homo sapiens', 'age_units': 'year'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        cell_line['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        cell_line['@id'],
        {'organism': 'Saccharomyces', 'age_units': 'year'}, expect_errors=True)
    assert(res.status_code == 422)


def test_lifestage_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'organism': 'Homo sapiens', 'life_stage': 'adult'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        cell_line['@id'],
        {'organism': 'Mus musculus', 'life_stage': 'stationary'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        cell_line['@id'],
        {'organism': 'Saccharomyces', 'life_stage': 'adult'}, expect_errors=True)
    assert(res.status_code == 422)


def test_nih_institutional_certification(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'nih_institutional_certification': 'NICHD1455'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        cell_line['@id'],
        {'nih_institutional_certification': 'ABBBCCCHD1455'}, expect_errors=True)
    assert(res.status_code == 422)


def test_collections(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'collections': ['ENCODE']})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        cell_line['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert(res.status_code == 422)
