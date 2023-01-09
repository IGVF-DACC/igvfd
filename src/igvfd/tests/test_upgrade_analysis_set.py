import pytest


def test_analysis_set_upgrade_1_2(upgrader, analysis_set_v1):
    alias = analysis_set_v1['aliases']
    alternate_accession = analysis_set_v1['alternate_accessions']
    collection = analysis_set_v1['collections']
    document = analysis_set_v1['documents']
    value = upgrader.upgrade('analysis_set', analysis_set_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'alternate_accessions' not in value
    assert alternate_accession == value['alternate_accession']
    assert 'collections' not in value
    assert collection == value['collection']
    assert 'documents' not in value
    assert document == value['document']
    assert value['schema_version'] == '2'
