import pytest


def test_file_set_type_dependency(analysis_set_base, measurement_set, testapp):
    res = testapp.patch_json(
        analysis_set_base['@id'],
        {'file_set_type': 'principal analysis'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        analysis_set_base['@id'],
        {'file_set_type': 'principal analysis',
         'input_file_sets': [measurement_set['@id']]})
    assert res.status_code == 200
