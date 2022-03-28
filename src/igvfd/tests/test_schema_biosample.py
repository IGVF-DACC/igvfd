import pytest


def test_sample_1(biosample_1, testapp):
    res = testapp.get(biosample_1['@id'])
    assert(res.json['accession'][:6] == 'IGVFSM')


def test_lot_id_dependency(biosample_1, testapp):
    res = testapp.patch_json(
        biosample_1['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)


def test_age_unit_dependency(biosample_1, testapp):
    res = testapp.patch_json(
        biosample_1['@id'],
        {'organism': 'Homo sapiens', 'age_units': 'year'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        biosample_1['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        biosample_1['@id'],
        {'organism': 'Saccharomyces', 'age_units': 'year'}, expect_errors=True)
    assert(res.status_code == 422)


def test_age_unit_dependency(biosample_1, testapp):
    print(biosample_1)
    res = testapp.patch_json(
        biosample_1['@id'],
        {'organism': 'Homo sapiens', 'life_stage': 'adult'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        biosample_1['@id'],
        {'organism': 'Mus musculus', 'life_stage': 'stationary'}, expect_errors=True)
    print(res.status_code)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        biosample_1['@id'],
        {'organism': 'Saccharomyces', 'life_stage': 'adult'}, expect_errors=True)
    print(res.status_code)
    assert(res.status_code == 422)
