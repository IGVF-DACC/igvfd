import pytest


def test_prediction_set_upgrade_1_2(upgrader, prediction_set_v1):
    value = upgrader.upgrade('prediction_set', prediction_set_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_prediction_set_upgrade_2_3(upgrader, prediction_set_v2):
    value = upgrader.upgrade('prediction_set', prediction_set_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value
