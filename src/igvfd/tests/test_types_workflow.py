import pytest


def test_analysis_steps_on_workflow(testapp, base_workflow_3, analysis_step):
    """Test that the analysis steps are correctly linked to the workflow.
    """
    res = testapp.get(base_workflow_3['@id'])
    assert set([item['@id'] for item in res.json.get('analysis_steps')]) == {analysis_step['@id']}
