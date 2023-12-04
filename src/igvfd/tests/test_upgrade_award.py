import pytest


def test_award_upgrade_1_2(upgrader, award_v1):
    value = upgrader.upgrade('award', award_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_award_upgrade_2_3(upgrader, award_v2):
    pis = award_v2['pi']
    value = upgrader.upgrade('award', award_v2, current_version='2', target_version='3')
    assert 'pi' not in value
    assert pis == value['pis']
    assert value['schema_version'] == '3'


def test_award_upgrade_2_3(upgrader, award_v3):
    value = upgrader.upgrade('award', award_v3, current_version='3', target_version='4')
    assert 'description' not in value
    assert value['schema_version'] == '4'
