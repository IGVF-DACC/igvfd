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


def test_analysis_step_upgrade_6_7(upgrader, analysis_step_v6):
    value = upgrader.upgrade('analysis_step', analysis_step_v6, current_version='6', target_version='7')
    assert sorted(value['input_content_types']) == sorted(['reads', 'kallisto single cell RNAseq output'])
    assert sorted(value['output_content_types']) == sorted(['alignments', 'kallisto single cell RNAseq output'])
    assert value['schema_version'] == '7'


def test_analysis_step_upgrade_8_9(upgrader, analysis_step_v8):
    assert 'workflow' in analysis_step_v8
    assert analysis_step_v8['schema_version'] == '8'
    value = upgrader.upgrade('analysis_step', analysis_step_v8, current_version='8', target_version='9')
    assert 'workflow' not in value
    assert value['schema_version'] == '9'
