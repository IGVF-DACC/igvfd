import pytest


def test_tabular_file_upgrade_1_2(upgrader, tabular_file_v1):
    value = upgrader.upgrade('tabular_file', tabular_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_tabular_file_upgrade_2_3(upgrader, tabular_file_v2):
    value = upgrader.upgrade('tabular_file', tabular_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'
