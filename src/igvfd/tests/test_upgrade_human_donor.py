import pytest


def test_human_donor_upgrade_1_2(upgrader, human_donor_1):
    value = upgrader.upgrade('human_donor', human_donor_1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert value['schema_version'] == '2'
