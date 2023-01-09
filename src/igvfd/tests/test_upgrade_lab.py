import pytest


def test_lab_upgrade_1_2(upgrader, lab_v1):
    value = upgrader.upgrade('lab', lab_v1, current_version='1', target_version='2')
    assert 'awards' not in value
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_lab_upgrade_2_3(upgrader, lab_v2):
    alias = lab_v2['aliases']
    award = lab_v2['awards']
    value = upgrader.upgrade('lab', lab_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'awards' not in value
    assert award == value['award']
    assert value['schema_version'] == '3'
