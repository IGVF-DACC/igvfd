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
        {'age': '1', 'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'minute'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Saccharomyces'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'age_units': 'year'}, expect_errors=True)
    assert res.status_code == 422
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


def test_lifestage_dependency(tissue, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Mus musculus'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'life_stage': 'embryonic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Homo sapiens', 'life_stage': 'fermentative'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Saccharomyces', 'life_stage': 'child'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Saccharomyces', 'life_stage': 'lag'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Homo sapiens'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'life_stage': 'unknown'})
    assert res.status_code == 200
    res = testapp.patch_json(
        tissue['@id'],
        {'taxa': 'Homo sapiens'})
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


def test_part_of_tissue(tissue, primary_cell_part_of, differentiated_cell, differentiated_tissue, cell_line, tissue_part_of, whole_organism_part_of, testapp):
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': differentiated_tissue['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tissue['@id'],
        {'part_of': cell_line['@id']}, expect_errors=True)
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
