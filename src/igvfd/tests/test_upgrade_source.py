import pytest


def test_source_upgrade_1_2(upgrader, source_1):
    value = upgrader.upgrade('source', source_1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
