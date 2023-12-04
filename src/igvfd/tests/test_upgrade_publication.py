import pytest


def test_publication_upgrade_1_2(upgrader, publication_v1):
    value = upgrader.upgrade('publication', publication_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_publication_upgrade_1_2(upgrader, publication_v2):
    ids = publication_v2['identifiers']
    value = upgrader.upgrade('publication', publication_v2, current_version='2', target_version='3')
    assert 'identifiers' not in value
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert value['schema_version'] == '3'


def test_publication_upgrade_1_2(upgrader, publication_v3):
    value = upgrader.upgrade('publication', publication_v3, current_version='3', target_version='4')
    assert 'description' not in value
    assert value['schema_version'] == '4'
