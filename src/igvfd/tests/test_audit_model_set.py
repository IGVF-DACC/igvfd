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


def test_audit_missing_input_file_set(
    testapp,
    model_set_no_input,
    analysis_set_base,
    model_file,
    signal_file
):
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    testapp.patch_json(
        model_file['@id'],
        {
            'file_set': model_set_no_input['@id'],
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': model_set_no_input['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_derived_from(
    testapp,
    model_set_no_input,
    model_file,
    signal_file
):
    testapp.patch_json(
        model_file['@id'],
        {
            'file_set': model_set_no_input['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        model_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_unexpected_input_file_set(
    testapp,
    model_set_no_input,
    model_file,
    signal_file,
    measurement_set_multiome
):
    testapp.patch_json(
        model_file['@id'],
        {
            'file_set': model_set_no_input['@id']
        }
    )
    testapp.patch_json(
        model_set_no_input['@id'],
        {
            'input_file_sets': [measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        model_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': measurement_set_multiome['@id']
        }
    )
    res = testapp.get(model_set_no_input['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', []))
