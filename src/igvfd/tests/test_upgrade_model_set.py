import pytest


def test_model_set_upgrade_1_2(upgrader, model_set_v1):
    value = upgrader.upgrade('model_set', model_set_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'description' not in value
