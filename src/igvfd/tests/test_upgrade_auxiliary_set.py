import pytest


def test_auxiliary_set_upgrade_1_2(upgrader, auxiliary_set_v1):
    ids = auxiliary_set_v1['references']
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_auxiliary_set_upgrade_2_3(upgrader, auxiliary_set_v2):
    old_auxiliary_type = auxiliary_set_v2['auxiliary_type']
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'file_set_type' in value and value['file_set_type'] == old_auxiliary_type
    assert 'auxiliary_type' not in value


def test_auxiliary_set_upgrade_3_4(upgrader, auxiliary_set_v3):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v3,
        current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'construct_libraries' not in value
    assert 'moi' not in value


def test_auxiliary_set_upgrade_4_5(upgrader, auxiliary_set_v4):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v4,
        current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'description' not in value
