import pytest


def test_model_upgrade_1_2(upgrader, model_v1):
    ids = model_v1['references']
    value = upgrader.upgrade(
        'prediction', model_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_model_upgrade_2_3(upgrader, model_v2):
    old_model_type = model_v2['model_type']
    value = upgrader.upgrade(
        'model', model_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'file_set_type' in value and value['file_set_type'] == old_model_type
    assert 'model_type' not in value
