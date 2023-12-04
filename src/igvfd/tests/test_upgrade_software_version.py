import pytest


def test_software_version_upgrade_1_2(upgrader, software_version_v1):
    ids = software_version_v1['references']
    value = upgrader.upgrade(
        'software_version', software_version_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_software_version_upgrade_2_3(upgrader, software_version_v2_no_v, software_version_v2):
    value = upgrader.upgrade(
        'software_version', software_version_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert value['version'] == 'v0.0.1'
    value = upgrader.upgrade(
        'software_version', software_version_v2_no_v,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert value['version'] == 'v2.4.4'


def test_software_version_upgrade_3_4(upgrader, software_version_v3):
    value = upgrader.upgrade(
        'software_version', software_version_v3,
        current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'description' not in value
