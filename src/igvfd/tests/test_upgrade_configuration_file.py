import pytest


def test_configuration_file_upgrade_1_2(upgrader, configuration_file_v1):
    value = upgrader.upgrade('configuration_file', configuration_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'
