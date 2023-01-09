import pytest


def test_reference_data_upgrade_1_2(upgrader, reference_data_v1):
    alias = reference_data_v1['aliases']
    alternate_accession = reference_data_v1['alternate_accessions']
    collection = reference_data_v1['collections']
    document = reference_data_v1['documents']
    value = upgrader.upgrade('reference_data', reference_data_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'alternate_accessions' not in value
    assert alternate_accession == value['alternate_accession']
    assert 'collections' not in value
    assert collection == value['collection']
    assert 'documents' not in value
    assert document == value['document']
    assert value['schema_version'] == '2'
