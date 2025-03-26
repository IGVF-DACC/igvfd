import pytest


def test_analysis_step_upgrade_1_2(upgrader, analysis_step_v1):
    value = upgrader.upgrade('analysis_step', analysis_step_v1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert value['analysis_step_types'] == ['alignment']
    assert value['input_content_types'] == ['reads']
    assert value['output_content_types'] == ['reads']
    assert value['schema_version'] == '2'


def test_analysis_step_upgrade_2_3(upgrader, analysis_step_v2):
    value = upgrader.upgrade('analysis_step', analysis_step_v2, current_version='2', target_version='3')
    assert value['lab'] == '/labs/j-michael-cherry/'
    assert value['award'] == '/awards/HG012012/'


def test_analysis_step_upgrade_5_6(upgrader, analysis_step_v5):
    value = upgrader.upgrade('analysis_step', analysis_step_v5, current_version='5', target_version='6')
    assert sorted(value['input_content_types']) == sorted(['reads', 'barcode onlist'])
    assert sorted(value['output_content_types']) == sorted(['alignments'])
    assert value['schema_version'] == '6'
