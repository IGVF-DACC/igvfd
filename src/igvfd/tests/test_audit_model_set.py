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
        for error in res.json['audit'].get('WARNING', [])
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
