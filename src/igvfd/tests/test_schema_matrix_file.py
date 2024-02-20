import pytest


def test_hic_dimension_dependency(testapp, matrix_file_hic):
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'dimension1': 'gene'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'dimension2': 'treatment'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        matrix_file_hic['@id'],
        {'dimension2': 'treatment',
         'file_format': 'mtx'})
    assert res.status_code == 200
