import pytest


def test_audit_missing_analysis_step_version_prediction_set(
    testapp,
    base_prediction_set,
    matrix_file,
    analysis_step_version
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': base_prediction_set['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing analysis step version'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step version'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_input_file_set(
    testapp,
    base_prediction_set,
    analysis_set_base,
    tabular_file,
    signal_file
):
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
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
        tabular_file['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': base_prediction_set['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_derived_from(
    testapp,
    base_prediction_set,
    tabular_file,
    signal_file
):
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': base_prediction_set['@id']
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_unexpected_input_file_set(
    testapp,
    base_prediction_set,
    tabular_file,
    signal_file,
    measurement_set_multiome
):
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': base_prediction_set['@id']
        }
    )
    testapp.patch_json(
        base_prediction_set['@id'],
        {
            'input_file_sets': [measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
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
    res = testapp.get(base_prediction_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', []))
