import pytest


def test_model_set_upgrade_1_2(upgrader, model_set_v1):
    value = upgrader.upgrade('model_set', model_set_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'description' not in value


def test_model_set_upgrade_3_4(upgrader, model_set_v3):
    value = upgrader.upgrade('model_set', model_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'publication_identifiers' not in value


def test_model_set_upgrade_4_5(upgrader, model_set_v4):
    value = upgrader.upgrade('model_set', model_set_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'software_version' not in value


def test_model_set_upgrade_5_6(upgrader, model_set_v5):
    value = upgrader.upgrade('model_set', model_set_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value.get('preferred_assay_titles') == ['10x scATAC with Scale pre-indexing']
    assert value.get('notes') == 'This model set previously used 10x with Scale pre-indexing as a preferred_assay_titles, but it has been updated to 10x scATAC with Scale pre-indexing via an upgrade.'
