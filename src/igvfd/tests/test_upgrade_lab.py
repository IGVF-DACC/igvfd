import pytest


def test_lab_upgrade_1_2(upgrader, lab_1):
    value = upgrader.upgrade('lab', lab_1, current_version='1', target_version='2')
    assert 'awards' not in value
    assert value['schema_version'] == '2'
