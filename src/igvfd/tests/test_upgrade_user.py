import pytest


def test_user_upgrade_1_2(upgrader, user_v1):
    value = upgrader.upgrade('user', user_v1, current_version='1', target_version='2')
    assert 'submits_for' not in value
    assert 'aliases' not in value
    assert 'groups' not in value
    assert value['schema_version'] == '2'


def test_user_upgrade_2_3(upgrader, user_v2):
    value = upgrader.upgrade('user', user_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_user_upgrade_3_4(upgrader, user_v3):
    value = upgrader.upgrade('user', user_v3, current_version='3', target_version='4')
    assert 'viewing_groups' not in value
    assert value['schema_version'] == '4'


def test_user_upgrade_4_5(upgrader, user_v4):
    value = upgrader.upgrade('user', user_v4, current_version='4', target_version='5')
    assert value['email'] == 'email_name@email_domain.com'
    assert value['schema_version'] == '5'
