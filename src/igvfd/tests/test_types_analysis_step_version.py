import pytest


def test_types_analysis_step_version_audit_calc_workflows(testapp, analysis_step_version_3, base_workflow_no_asv, base_workflow_2):
    # Test: No workflows calculated on ASV if this ASV is not linked to any workflow
    res = testapp.get(analysis_step_version_3['@id'])
    assert res.json['workflows'] == []

    # Test: if an ASV is linked to a single workflow
    testapp.patch_json(
        base_workflow_no_asv['@id'],
        {
            'analysis_step_versions': [
                analysis_step_version_3['@id']
            ]
        }
    )
    res = testapp.get(analysis_step_version_3['@id'])
    assert len(res.json['workflows']) == 1
    assert res.json['workflows'][0]['@id'] == base_workflow_no_asv['@id']
    # Test: if one ASV is linked to multiple workflows
    testapp.patch_json(
        base_workflow_2['@id'],
        {
            'analysis_step_versions': [
                analysis_step_version_3['@id']
            ]
        }
    )
    res = testapp.get(analysis_step_version_3['@id'])
    assert len(res.json['workflows']) == 2
