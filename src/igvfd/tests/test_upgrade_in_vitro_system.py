import pytest


def test_in_vitro_system_upgrade_1_2(upgrader, in_vitro_system_v1):
    assert 'donor' in in_vitro_system_v1
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v1, current_version='1', target_version='2')
    assert 'donor' not in value
    assert 'donors' in value
    assert value['schema_version'] == '2'


def test_in_vitro_system_upgrade_2_3(upgrader, in_vitro_system_v2):
    biomarkers = in_vitro_system_v2['biomarker']
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v2, current_version='2', target_version='3')
    assert 'biomarker' not in value
    assert biomarkers == value['biomarkers']
    assert value['schema_version'] == '3'
