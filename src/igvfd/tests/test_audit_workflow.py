import pytest


def test_audit_workflow_without_asvs(testapp, base_workflow, analysis_step_version, analysis_step_version_2):
    # Test: workflow without analysis step versions (flag)
    res = testapp.get(base_workflow['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing analysis step versions'
        for error in res.json['audit'].get('WARNING', [])
    )

    # Test: workflow with one analysis step version (no flag)
    testapp.patch_json(base_workflow['@id'], {
        'analysis_step_versions': [analysis_step_version['@id']]
    })
    res = testapp.get(base_workflow['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step versions'
        for error in res.json['audit'].get('WARNING', [])
    )

    # Test: workflow with two analysis step version (no flag)
    testapp.patch_json(base_workflow['@id'],
                       {'analysis_step_versions': [analysis_step_version['@id'],
                                                   analysis_step_version_2['@id']]}
                       )
    res = testapp.get(base_workflow['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step versions'
        for error in res.json['audit'].get('WARNING', [])
    )
