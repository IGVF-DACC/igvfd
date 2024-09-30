import pytest


def test_hic_dimension_dependency(testapp, matrix_file_hic):
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'principal_dimension': 'gene'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'secondary_dimensions': ['treatment']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'secondary_dimensions': ['treatment'],
         'file_format': 'mtx'})
    assert res.status_code == 200
