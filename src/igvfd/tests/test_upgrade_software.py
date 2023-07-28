import pytest


def test_software_upgrade_1_2(upgrader, software_v1):
    ids = software_v1['identifiers']
    value = upgrader.upgrade(
        'software', software_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value
