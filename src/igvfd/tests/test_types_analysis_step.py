import pytest


def test_analysis_step_name_calcprop(testapp, analysis_step):
    assert analysis_step['@id'] == '/analysis-steps/base-analysis-step-v-1/'
    assert analysis_step['name'] == 'workflow-base-analysis-step'
    assert analysis_step['major_version'] == 1
