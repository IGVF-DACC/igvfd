import pytest


def test_accession(organism1, testapp):
    res = testapp.get(organism1['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(organism1, testapp):
    res = testapp.patch_json(
        organism1['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_description(organism1, testapp):
    res = testapp.patch_json(
        organism1['@id'],
        {'description': 'I am a modern major general.'})
    assert res.status_code == 200


def test_failure_patch_calculated_sex(organism1, testapp):
    res = testapp.patch_json(
        organism1['@id'],
        {'sex': 'female'}, expect_errors=True)
    assert res.status_code == 422


def test_lifestage_dependency(organism1, testapp):
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        organism1['@id'],
        {'life_stage': 'embryonic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Homo sapiens', 'life_stage': 'fermentative'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Saccharomyces', 'life_stage': 'child'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Saccharomyces', 'life_stage': 'lag'})
    assert res.status_code == 200
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Homo sapiens'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        organism1['@id'],
        {'life_stage': 'unknown'})
    assert res.status_code == 200
    res = testapp.patch_json(
        organism1['@id'],
        {'organism': 'Homo sapiens'})
    assert res.status_code == 200


def test_collections(organism1, testapp):
    res = testapp.patch_json(
        organism1['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        organism1['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422
