import pytest


def test_gene_upgrade_1_2(upgrader, gene_v1):
    value = upgrader.upgrade('gene', gene_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_gene_upgrade_2_3(upgrader, gene_v2):
    value = upgrader.upgrade('gene', gene_v2, current_version='2', target_version='3')
    assert value['geneid'].startswith('ENS')
    assert value['schema_version'] == '3'


def test_gene_upgrade_3_4(upgrader, gene_v3):
    alias = gene_v3['aliases']
    synonym = gene_v3['synonyms']
    dbxref = gene_v3['dbxrefs']
    location = gene_v3['locations']
    value = upgrader.upgrade('gene', gene_v3, current_version='3', target_version='4')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'synonyms' not in value
    assert synonym == value['synonym']
    assert 'dbxrefs' not in value
    assert dbxref == value['dbxref']
    assert 'locations' not in value
    assert location == value['location']
    assert value['schema_version'] == '4'
