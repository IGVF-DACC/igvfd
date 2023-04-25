import pytest


def test_accession(tissue, testapp):
    res = testapp.get(tissue['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_nih_institutional_certification(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'nih_institutional_certification': 'NICHD1455'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'nih_institutional_certification': 'ABBBCCCHD1455'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_failure_patch_calculated_sex(testapp, tissue):
    res = testapp.patch_json(
        tissue['@id'],
        {'sex': 'female'}, expect_errors=True)
    assert res.status_code == 422


def test_part_of_tissue(tissue, primary_cell_part_of, in_vitro_differentiated_cell, in_vitro_organoid, in_vitro_cell_line, tissue_part_of, whole_organism_part_of, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': in_vitro_differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': in_vitro_organoid['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': in_vitro_cell_line['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of':  primary_cell_part_of['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of':  tissue_part_of['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of':  whole_organism_part_of['@id']})
    assert res.status_code == 200


def test_sorted_fraction_detail_dependency(testapp, tissue, primary_cell):
    res = testapp.patch_json(
        tissue['@id'],
        {'sorted_fraction': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'sorted_fraction_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'sorted_fraction': primary_cell['@id'],
         'sorted_fraction_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200
