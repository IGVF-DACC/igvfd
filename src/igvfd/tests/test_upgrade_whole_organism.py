import pytest


def test_whole_organism_upgrade_1_2(upgrader, whole_organism_1):
    value = upgrader.upgrade('whole_organism', whole_organism_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_whole_organism_upgrade_2_3(upgrader, whole_organism_2):
    value = upgrader.upgrade('whole_organism', whole_organism_2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert 'donors' not in value
    assert 'dbxrefs' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'treatments' not in value
    assert value['schema_version'] == '3'
