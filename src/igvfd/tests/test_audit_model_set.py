import pytest


def test_audit_external_input_data_content_type(
    testapp,
    model_set_no_input,
    tabular_file
):
    testapp.patch_json(
        model_set_no_input['@id'],
        {
            'external_input_data': tabular_file['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent external input data'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'content_type': 'external source data'
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent external input data'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_analysis_step_version_model_set(
    testapp,
    model_set_no_input,
    matrix_file,
    analysis_step_version
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': model_set_no_input['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing analysis step version'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step version'
        for error in res.json['audit'].get('WARNING', [])
    )
