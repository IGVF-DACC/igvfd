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


def test_rodent_donor_upgrade_2_3(upgrader, rodent_donor_v2):
    alias = rodent_donor_v2['aliases']
    alternate_accession = rodent_donor_v2['alternate_accessions']
    collection = rodent_donor_v2['collections']
    document = rodent_donor_v2['documents']
    reference = rodent_donor_v2['references']
    trait = rodent_donor_v2['traits']
    external_resource = rodent_donor_v2['external_resources']
    value = upgrader.upgrade('rodent_donor', rodent_donor_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'alternate_accessions' not in value
    assert alternate_accession == value['alternate_accession']
    assert 'collections' not in value
    assert collection == value['collection']
    assert 'documents' not in value
    assert document == value['document']
    assert 'references' not in value
    assert reference == value['reference']
    assert 'traits' not in value
    assert trait == value['trait']
    assert 'external_resources' not in value
    assert external_resource == value['external_resource']
    assert value['schema_version'] == '3'
