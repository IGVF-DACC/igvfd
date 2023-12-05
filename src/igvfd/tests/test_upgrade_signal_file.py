import pytest


def test_signal_file_upgrade_1_2(upgrader, signal_file_v1):
    value = upgrader.upgrade('signal_file', signal_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_signal_file_upgrade_2_3(upgrader, signal_file_v2):
    value = upgrader.upgrade('signal_file', signal_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'
