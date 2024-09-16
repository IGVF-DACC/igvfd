import pytest


def test_audit_missing_input_file_set(
    testapp,
    analysis_set_base,
    measurement_set,
    matrix_file,
    signal_file
):
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_derived_from(
    testapp,
    analysis_set_base,
    matrix_file,
    signal_file
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing derived from'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_unexpected_input_file_set(
    testapp,
    analysis_set_base,
    matrix_file,
    signal_file,
    measurement_set_multiome
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
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
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_analysis_step_version(
    testapp,
    intermediate_analysis_set,
    matrix_file,
    analysis_step_version
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': intermediate_analysis_set['@id']
        }
    )
    res = testapp.get(intermediate_analysis_set['@id'] + '@@audit')
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
    res = testapp.get(intermediate_analysis_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step version'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_multiple_workflows(
    testapp,
    analysis_set_with_workflow,
    matrix_file_with_base_workflow,
    matrix_file_with_base_workflow_2
):
    # Test when an analysis set only has one workflow
    res = testapp.get(analysis_set_with_workflow['@id'] + '@@audit')
    assert any(
        error['category'] != 'unexpected workflows'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Patching 2 matrix files to a single analysis set
    # Two workflows for a single analysis set
    testapp.patch_json(
        matrix_file_with_base_workflow['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    testapp.patch_json(
        matrix_file_with_base_workflow_2['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    res = testapp.get(analysis_set_with_workflow['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected workflows'
        for error in res.json['audit'].get('WARNING', [])
    )
