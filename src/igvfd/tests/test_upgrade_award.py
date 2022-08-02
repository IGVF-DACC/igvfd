import pytest


def test_award_upgrade_1_2(upgrader, award_v1):
    value = upgrader.upgrade('award', award_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
