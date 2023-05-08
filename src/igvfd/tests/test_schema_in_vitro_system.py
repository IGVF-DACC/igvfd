import pytest


def test_passage_number_dependency(in_vitro_cell_line, testapp):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'passage_number': 3})
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'classification': 'differentiated cell'}, expect_errors=True)
    assert res.status_code == 422


def test_time_post_factors_dependency(in_vitro_differentiated_cell, treatment_chemical, testapp):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'introduced_factors': [treatment_chemical['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3, 'time_post_factors_introduction_units': 'day', 'introduced_factors': [treatment_chemical['@id']]})
    assert res.status_code == 200


def test_sorted_fraction(testapp, in_vitro_organoid, in_vitro_differentiated_cell):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_fraction': in_vitro_organoid['@id'],
         'sorted_fraction_detail': 'default test description'}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_fraction': 'I am just pretending to be a sorted fraction parent.',
         'sorted_fraction_detail': 'default test description'}, expect_errors=True)
    assert res.status_code == 422


def test_sorted_fraction_detail_dependency(testapp, in_vitro_organoid, primary_cell):
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_fraction': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_fraction_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_fraction': primary_cell['@id'],
         'sorted_fraction_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200


def test_cellular_sub_pool(testapp, in_vitro_differentiated_cell, primary_cell, in_vitro_organoid):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'cellular_sub_pool': 'SS-PKR_1'}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'cellular_sub_pool': 'SS-PKR_1'}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'cellular_sub_pool': 'LW231B-2'}, expect_errors=True)
    assert res.status_code == 200
