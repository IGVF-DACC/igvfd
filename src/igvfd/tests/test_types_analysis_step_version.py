import pytest


def test_analysis_step_version_name(testapp, analysis_step_version):
    res = testapp.get(analysis_step_version['@id'])
    assert res.json.get('name') == 'IGVFWF0000WRKF-base-analysis-step-2023-07-12'
