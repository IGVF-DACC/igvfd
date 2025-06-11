import pytest


def test_calc_analysis_steps_on_workflow(testapp, base_workflow, analysis_step_version, analysis_step_version_2, analysis_step, analysis_step_2):
    """Test that the audit calculation for workflows works correctly."""
    # Create a workflow with an analysis step version
    res = testapp.get(base_workflow['@id'])
    assert res.json['analysis_steps'] == []

    # Workflows with one analysis step version
    testapp.patch_json(base_workflow['@id'],
                       {'analysis_step_versions': [analysis_step_version['@id']]}
                       )
    res = testapp.get(base_workflow['@id'])
    assert sorted([item['@id'] for item in res.json['analysis_steps']]) == [analysis_step['@id']]

    # Workflows with multiple analysis step version
    testapp.patch_json(base_workflow['@id'],
                       {'analysis_step_versions': [analysis_step_version['@id'],
                                                   analysis_step_version_2['@id']]}
                       )
    res = testapp.get(base_workflow['@id'])
    assert sorted([item['@id'] for item in res.json['analysis_steps']]
                  ) == sorted([analysis_step['@id'], analysis_step_2['@id']])
