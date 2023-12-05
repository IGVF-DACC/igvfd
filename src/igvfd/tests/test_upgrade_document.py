import pytest


def test_document_upgrade_1_2(upgrader, document_v1):
    value = upgrader.upgrade('document', document_v1, current_version='1', target_version='2')
    assert 'urls' not in value
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_document_upgrade_2_3(upgrader, document_v2):
    value = upgrader.upgrade('document', document_v2, current_version='2', target_version='3')
    assert value['description'] == 'Default upgrade text: please add details about document in description.'
    assert value['schema_version'] == '3'
