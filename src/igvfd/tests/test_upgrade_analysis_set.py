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
