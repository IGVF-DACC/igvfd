import pytest


def test_lab_upgrade_1_2(upgrader, lab_v1):
    value = upgrader.upgrade('lab', lab_v1, current_version='1', target_version='2')
    assert 'awards' not in value
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_lab_upgrade_2_3(upgrader, lab_v2):
    value = upgrader.upgrade('lab', lab_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value
