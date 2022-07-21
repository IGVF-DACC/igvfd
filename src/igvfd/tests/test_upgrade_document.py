import pytest


def test_document_upgrade_1_2(upgrader, document_1):
    value = upgrader.upgrade('document', document_1, current_version='1', target_version='2')
    assert 'urls' not in value
    assert value['schema_version'] == '2'
