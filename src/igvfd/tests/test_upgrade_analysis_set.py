import pytest


def test_analysis_set_upgrade_1_2(upgrader, analysis_set_v1):
    samples = analysis_set_v1['sample']
    donors = analysis_set_v1['donor']
    input_file_sets = analysis_set_v1['input_file_set']
    value = upgrader.upgrade('analysis_set', analysis_set_v1, current_version='1', target_version='2')
    assert 'sample' not in value
    assert samples == value['samples']
    assert 'donor' not in value
    assert donors == value['donors']
    assert 'input_file_set' not in value
    assert input_file_sets == value['input_file_sets']
    assert value['schema_version'] == '2'


def test_analysis_set_upgrade_3_4(upgrader, analysis_set_v3):
    assert 'file_set_type' not in analysis_set_v3
    value = upgrader.upgrade('analysis_set', analysis_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert value['file_set_type'] == 'intermediate analysis'


def test_analysis_set_upgrade_4_5(upgrader, analysis_set_v4):
    value = upgrader.upgrade('analysis_set', analysis_set_v4, current_version='4', target_version='5')
    assert 'description' not in value
    assert value['schema_version'] == '5'


def test_analysis_set_upgrade_6_7(upgrader, analysis_set_v6):
    value = upgrader.upgrade('analysis_set', analysis_set_v6, current_version='6', target_version='7')
    assert value['file_set_type'] == 'principal analysis'
    assert value['schema_version'] == '7'
    assert value['notes'].endswith('file_set_type was primary analysis and has been updated to be principal analysis.')


def test_analysis_set_upgrade_7_8(upgrader, analysis_set_v7):
    value = upgrader.upgrade('analysis_set', analysis_set_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert 'publication_identifiers' not in value


def test_analysis_set_upgrade_8_9(upgrader, analysis_set_v8):
    value = upgrader.upgrade('analysis_set', analysis_set_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'samples' not in value


def test_analysis_set_upgrade_9_10(upgrader, analysis_set_v9):
    value = upgrader.upgrade('analysis_set', analysis_set_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert 'demultiplexed_sample' not in value
    assert 'demultiplexed_samples' in value
    assert len(value['demultiplexed_samples']) == 1
