import pytest


def test_software_upgrade_1_2(upgrader, software_v1):
    ids = software_v1['references']
    value = upgrader.upgrade(
        'software', software_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_software_upgrade_2_3(upgrader, software_v2):
    value = upgrader.upgrade(
        'software', software_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value


def test_software_upgrade_4_5(upgrader, software_v4):
    value = upgrader.upgrade('software', software_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'used_by' not in value
