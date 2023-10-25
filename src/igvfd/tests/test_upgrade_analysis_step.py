import pytest


def test_analysis_step_upgrade_1_2(upgrader, analysis_step_v1):
    value = upgrader.upgrade('analysis_step', analysis_step_v1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert value['analysis_step_types'] == 'alignment'
    assert value['input_content_types'] == 'reads'
    assert value['output_content_types'] == 'reads'
    assert value['schema_version'] == '2'
