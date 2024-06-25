import pytest


def test_analysis_step_version_name(testapp, analysis_step_version):
    res = testapp.get(analysis_step_version['@id'])
    print(res.json)
    assert res.json.get('name') == 'base-analysis-step-2023-07-12'
