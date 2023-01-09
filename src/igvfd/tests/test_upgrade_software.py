import pytest


def test_software_upgrade_1_2(upgrader, software_v1):
    alias = software_v1['aliases']
    reference = software_v1['references']
    value = upgrader.upgrade('software', software_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'references' not in value
    assert reference == value['reference']
    assert value['schema_version'] == '2'
