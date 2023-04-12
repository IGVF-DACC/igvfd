import pytest


def test_measurement_set_upgrade_1_2(upgrader, measurement_set_v1):
    samples = measurement_set_v1['sample']
    donors = measurement_set_v1['donor']
    value = upgrader.upgrade('measurement_set', measurement_set_v1, current_version='1', target_version='2')
    assert 'sample' not in value
    assert samples == value['samples']
    assert 'donor' not in value
    assert donors == value['donors']
    assert value['schema_version'] == '2'


def test_measurement_set_upgrade_3_4(upgrader, measurement_set_v3):
    value = upgrader.upgrade('measurement_set', measurement_set_v3, current_version='3', target_version='4')
    assert 'protocol' not in value
    assert value['schema_version'] == '4'
