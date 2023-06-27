import pytest


def test_analysis_step_name_calcprop(testapp, analysis_step):
    res = testapp.get(analysis_step['@id'])
    assert res.json.get('name') == 'IGVFWF0000WRKF-base-analysis-step'
