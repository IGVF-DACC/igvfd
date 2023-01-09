import pytest


def test_user_upgrade_1_2(upgrader, user_v1):
    value = upgrader.upgrade('user', user_v1, current_version='1', target_version='2')
    assert 'submits_for' not in value
    assert 'aliases' not in value
    assert 'groups' not in value
    assert value['schema_version'] == '2'


def test_user_upgrade_2_3(upgrader, user_v2):
    alias = user_v2['aliases']
    group = user_v2['groups']
    viewing_group = user_v2['viewing_groups']
    value = upgrader.upgrade('user', user_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'groups' not in value
    assert group == value['group']
    assert 'viewing_groups' not in value
    assert viewing_group == value['viewing_group']
    assert value['schema_version'] == '3'
