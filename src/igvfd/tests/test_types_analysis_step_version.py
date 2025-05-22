import pytest


def test_audit_calc_workflows(testapp, analysis_step_version, base_workflow, base_workflow_2):
    # Test: No workflows calculated on ASV if this ASV is not linked to any workflow
    res = testapp.get(analysis_step_version['@id'])
    assert res.json['workflows'] == []

    # Test: if an ASV is linked to a single workflow
    testapp.patch_json(base_workflow['@id'],
                       {'analysis_step_versions': [analysis_step_version['@id']]}
                       )
    res = testapp.get(analysis_step_version['@id'])
    assert res.json['workflows'] == [base_workflow['@id']]

    # Test: if one ASV is linked to multiple workflows
    testapp.patch_json(base_workflow_2['@id'],
                       {'analysis_step_versions': [analysis_step_version['@id']]}
                       )
    res = testapp.get(analysis_step_version['@id'])
    assert sorted(res.json['workflows']) == sorted([base_workflow['@id'], base_workflow_2['@id']])
