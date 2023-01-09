import pytest


def test_publication_upgrade_1_2(upgrader, publication_v1):
    value = upgrader.upgrade('publication', publication_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_document_upgrade_2_3(upgrader, publication_v2):
    alias = publication_v2['aliases']
    identifier = publication_v2['identifiers']
    value = upgrader.upgrade('publication', publication_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'identifiers' not in value
    assert identifier == value['identifier']
    assert value['schema_version'] == '3'
