import pytest


def test_gene_upgrade_1_2(upgrader, gene_1):
    value = upgrader.upgrade('gene', gene_1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
