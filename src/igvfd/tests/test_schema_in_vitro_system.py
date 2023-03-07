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


def test_time_post_factors_dependency(in_vitro_differentiated_cell, testapp):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3, 'time_post_factors_introduction_units': 'day'}, expect_errors=True)
    assert res.status_code == 200


def test_sorted_fraction(testapp, in_vitro_differentiated_tissue, in_vitro_differentiated_cell):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_fraction': in_vitro_differentiated_tissue['@id']}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_fraction': 'I am just pretending to be a sorted fraction parent.'}, expect_errors=True)
    assert res.status_code == 422
