import pytest


def test_accession(tissue, testapp):
    res = testapp.get(tissue['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_age_unit_dependency(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'lower_bound_age': 5, 'upper_bound_age': 10, 'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'minute'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Saccharomyces'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Homo sapiens', 'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'hour'})
    assert res.status_code == 200


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


def test_ccf_id(testapp, tissue, human_tissue):
    res = testapp.patch_json(
        human_tissue['@id'],
        {'ccf_id': '74c1e7c9-9cb0-47d0-93f8-e2cadef1cd86'})
    assert res.status_code == 200
    res = testapp.patch_json(
        human_tissue['@id'],
        {'ccf_id': 'this is really not a valid uuid'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'ccf_id': '84ff6a07-1dd8-452b-a99a-5042ac4a0f92'}, expect_errors=True)
    assert res.status_code == 422


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
