import pytest


def test_analysis_step_name_calcprop(testapp, analysis_step):
    res = testapp.get(analysis_step['@id'])
    assert res.json.get('name') == 'base-analysis-step'


def test_analysis_step_versions(testapp, analysis_step, analysis_step_version):
    res = testapp.get(analysis_step['@id'])
    assert set([analysis_step_version_item['@id']
               for analysis_step_version_item in res.json.get('analysis_step_versions')]) == {analysis_step_version['@id']}


def test_analysis_step_workflows(testapp, analysis_step, base_workflow_3):
    """Test that the analysis step is correctly linked to the workflow.
    """
    res = testapp.get(analysis_step['@id']).json
    assert sorted(set(res.get('workflows'))) == sorted(set([base_workflow_3['@id']]))
