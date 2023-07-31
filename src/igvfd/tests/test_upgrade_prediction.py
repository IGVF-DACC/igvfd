import pytest


def test_prediction_upgrade_1_2(upgrader, prediction_v1):
    ids = prediction_v1['references']
    value = upgrader.upgrade(
        'prediction', prediction_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value
