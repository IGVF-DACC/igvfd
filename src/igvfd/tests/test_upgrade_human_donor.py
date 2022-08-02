import pytest


def test_human_donor_upgrade_1_2(upgrader, human_donor_v1):
    value = upgrader.upgrade('human_donor', human_donor_v1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert 'external_resources' not in value
    assert 'aliases' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'documents' not in value
    assert 'references' not in value
    assert value['schema_version'] == '2'
