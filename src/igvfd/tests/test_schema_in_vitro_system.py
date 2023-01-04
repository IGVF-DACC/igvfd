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


def test_age_unit_dependency(in_vitro_cell_line, testapp):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'time_post_factors_introduction': 3}, expected_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'time_post_factors_introduction': 3, 'time_post_factors_introduction_units': 'day'}, expect_errors=True)
    assert res.status_code == 200
