import pytest


def test_source_upgrade_1_2(upgrader, source_v1):
    value = upgrader.upgrade('source', source_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_source_upgrade_2_3(upgrader, source_v2):
    value = upgrader.upgrade('source', source_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'
