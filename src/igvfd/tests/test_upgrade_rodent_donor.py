import pytest


def test_rodent_donor_upgrade_1_2(upgrader, rodent_donor_1):
    value = upgrader.upgrade('rodent_donor', rodent_donor_1, current_version='1', target_version='2')
    assert 'documents' not in value
    assert value['schema_version'] == '2'
