import pytest


def test_accession(whole_organism, testapp):
    res = testapp.get(whole_organism['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_description(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'description': 'I am a modern major general.'})
    assert res.status_code == 200


def test_failure_patch_calculated_sex(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sex': 'female'}, expect_errors=True)
    assert res.status_code == 422


def test_taxa_dependency(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'taxa': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism['@id'],
        {'taxa': 'Saccharomyces'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_sorted_fraction_detail_dependency(testapp, whole_organism, primary_cell):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_fraction': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_fraction_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_fraction': primary_cell['@id'],
         'sorted_fraction_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200
