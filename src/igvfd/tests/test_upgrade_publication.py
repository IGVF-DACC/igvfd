import pytest


def test_publication_upgrade_1_2(upgrader, publication_v1):
    value = upgrader.upgrade('publication', publication_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
