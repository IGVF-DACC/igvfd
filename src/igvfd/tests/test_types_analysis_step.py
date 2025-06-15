import pytest


def test_analysis_step_versions(testapp, analysis_step, analysis_step_version):
    res = testapp.get(analysis_step['@id'])
    assert set([analysis_step_version_item['@id']
               for analysis_step_version_item in res.json.get('analysis_step_versions')]) == {analysis_step_version['@id']}
