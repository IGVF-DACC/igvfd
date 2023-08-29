import pytest


def test_prediction_upgrade_1_2(upgrader, prediction_v1):
    ids = prediction_v1['references']
    value = upgrader.upgrade(
        'prediction', prediction_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_auxiliary_set_upgrade_2_3(upgrader, prediction_v2):
    old_prediction_type = prediction_v2['prediction_type']
    value = upgrader.upgrade(
        'prediction', prediction_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'file_set_type' in value and value['file_set_type'] == old_prediction_type
    assert 'prediction_type' not in value
