import pytest


def test_rodent_donor_upgrade_1_2(upgrader, rodent_donor_v1):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v1, current_version='1', target_version='2')
    assert 'documents' not in value
    assert 'parents' not in value
    assert 'external_resources' not in value
    assert 'aliases' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'references' not in value
    assert value['schema_version'] == '2'
