import pytest


def test_gene_upgrade_1_2(upgrader, gene_v1):
    value = upgrader.upgrade('gene', gene_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_gene_upgrade_2_3(upgrader, gene_v2):
    value = upgrader.upgrade('gene', gene_v2, current_version='2', target_version='3')
    assert value['geneid'].startswith('ENSEMBL')
    assert value['schema_version'] == '3'
