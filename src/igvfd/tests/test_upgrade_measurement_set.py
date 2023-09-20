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


def test_measurement_set_upgrade_4_5(upgrader, measurement_set_v4):
    value = upgrader.upgrade('measurement_set', measurement_set_v4, current_version='4', target_version='5')
    assert 'seqspec' not in value
    assert value['schema_version'] == '5'


def test_measurement_set_upgrade_5_6(upgrader, measurement_set_v5):
    value = upgrader.upgrade('measurement_set', measurement_set_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
