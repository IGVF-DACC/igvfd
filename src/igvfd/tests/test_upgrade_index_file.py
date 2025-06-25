import pytest


def test_index_file_upgrade_2_3(upgrader, index_file_v2):
    value = upgrader.upgrade('index_file', index_file_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert value['release_timestamp'] == '2025-06-24T12:34:56Z'
    assert value['notes'] == "This object's release_timestamp has been set to 2025-06-24T12:34:56Z"
