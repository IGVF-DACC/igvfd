import pytest


def test_sample_1(primary_cell, testapp):
    res = testapp.get(primary_cell['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_age_unit_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'taxa': 'Homo sapiens', 'lower_bound_age': 5, 'upper_bound_age': 10, 'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'taxa': 'Saccharomyces', 'age_units': 'year'}, expect_errors=True)
    assert res.status_code == 422


def test_nih_institutional_certification(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'nih_institutional_certification': 'NICHD1455'})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'nih_institutional_certification': 'ABBBCCCHD1455'}, expect_errors=True)
    assert res.status_code == 422


def test_pooled_from(primary_cell, tissue, pooled_from_primary_cell, pooled_from_primary_cell_2, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id']]}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id'], tissue['@id']]}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id'], pooled_from_primary_cell_2['@id']]})
    assert(res.status_code == 200)


def test_collection(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collection': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collection': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_part_of_primary_cell(primary_cell, primary_cell_part_of, differentiated_cell, differentiated_tissue, cell_line, tissue_part_of, whole_organism_part_of, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': differentiated_tissue['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': cell_line['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  primary_cell_part_of['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  tissue_part_of['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  whole_organism_part_of['@id']})
    assert res.status_code == 200
