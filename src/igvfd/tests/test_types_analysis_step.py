import pytest


def test_analysis_step_name_calcprop(testapp, analysis_step):
    res = testapp.get(analysis_step['@id'])
    assert res.json.get('name') == 'IGVFWF0000WRKF-base-analysis-step'


def test_analysis_step_versions(testapp, analysis_step, analysis_step_version):
    res = testapp.get(analysis_step['@id'])
    assert set([analysis_step_version_item['@id']
               for analysis_step_version_item in res.json.get('analysis_step_versions')]) == {analysis_step_version['@id']}


def test_as_workflows(testapp, analysis_step, base_workflow_3):
    res = testapp.get(analysis_step['@id'])
    assert set(res.json.get['workflows']) == sorted([base_workflow_3['@id']])
