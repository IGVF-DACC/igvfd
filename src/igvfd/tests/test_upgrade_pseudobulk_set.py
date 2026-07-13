import pytest


def test_pseudobulk_set_upgrade_1_2(upgrader, pseudobulk_set_v1):
    value = upgrader.upgrade('pseudobulk_set', pseudobulk_set_v1, current_version='1', target_version='2')
    assert value['merged'] is False
    assert value['schema_version'] == '2'
