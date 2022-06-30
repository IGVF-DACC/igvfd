import pytest


def test_accession(whole_organism1, testapp):
    res = testapp.get(whole_organism1['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_description(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'description': 'I am a modern major general.'})
    assert res.status_code == 200


def test_failure_patch_calculated_sex(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'sex': 'female'}, expect_errors=True)
    assert res.status_code == 422


def test_taxa_dependency(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Saccharomyces'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Homo sapiens'}, expect_errors=True)
    assert res.status_code == 422


def test_lifestage_dependency(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'life_stage': 'embryonic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'life_stage': 'child'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Saccharomyces', 'life_stage': 'child'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'taxa': 'Saccharomyces', 'life_stage': 'lag'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'life_stage': 'unknown'})
    assert res.status_code == 200


def test_collections(whole_organism1, testapp):
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism1['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422
