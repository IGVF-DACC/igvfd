import pytest


def test_access_key_upgrade_1_2(upgrader, access_key_1):
    value = upgrader.upgrade('access_key', access_key_1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
