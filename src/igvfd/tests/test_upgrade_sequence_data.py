import pytest


def test_sequence_data_upgrade_1_2(upgrader, sequence_data_v1):
    alias = sequence_data_v1['aliases']
    alternate_accession = sequence_data_v1['alternate_accessions']
    collection = sequence_data_v1['collections']
    document = sequence_data_v1['documents']
    dbxref = sequence_data_v1['dbxrefs']
    value = upgrader.upgrade('sequence_data', sequence_data_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'alternate_accessions' not in value
    assert alternate_accession == value['alternate_accession']
    assert 'collections' not in value
    assert collection == value['collection']
    assert 'documents' not in value
    assert document == value['document']
    assert 'dbxrefs' not in value
    assert dbxref == value['dbxref']
    assert value['schema_version'] == '2'
