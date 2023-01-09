import pytest


def test_curated_set_upgrade_1_2(upgrader, curated_set_v1):
    alias = curated_set_v1['aliases']
    alternate_accession = curated_set_v1['alternate_accessions']
    collection = curated_set_v1['collections']
    document = curated_set_v1['documents']
    reference = curated_set_v1['references']
    value = upgrader.upgrade('curated_set', curated_set_v1, current_version='1', target_version='2')
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
    assert value['schema_version'] == '2'
