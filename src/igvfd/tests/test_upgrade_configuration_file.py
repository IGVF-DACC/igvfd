import pytest


def test_configuration_file_upgrade_1_2(upgrader, configuration_file_v1):
    value = upgrader.upgrade('configuration_file', configuration_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_configuration_file_upgrade_2_3(upgrader, configuration_file_v2):
    value = upgrader.upgrade('configuration_file', configuration_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_configuration_file_upgrade_3_4(upgrader, configuration_file_v3):
    value = upgrader.upgrade('configuration_file', configuration_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_configuration_file_upgrade_6_7(upgrader, configuration_file_v6):
    value = upgrader.upgrade('configuration_file', configuration_file_v6, current_version='6', target_version='7')
    assert 'seqspec_of' not in value
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '7'


def test_configuration_file_upgrade_8_9(upgrader, configuration_file_v8):
    value = upgrader.upgrade('configuration_file', configuration_file_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert value['release_timestamp'] == '2025-06-24T12:34:56Z'
    assert value['notes'] == "This object's release_timestamp has been set to 2025-06-24T12:34:56Z"
