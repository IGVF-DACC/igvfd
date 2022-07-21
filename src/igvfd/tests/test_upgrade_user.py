import pytest


def test_user_upgrade_1_2(upgrader, user_1):
    value = upgrader.upgrade('user', user_1, current_version='1', target_version='2')
    assert 'submits_for' not in value
    assert value['schema_version'] == '2'
