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
    value = upgrader.upgrade('gene', gene_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert value['geneid'] == 'ENSMUSG00000004231'
    assert value['version_number'] == '8'
    assert value['annotation_version'] == 'GENCODE M30'


def test_gene_upgrade_4_5(upgrader, gene_v4):
    annotation = gene_v4['annotation_version']
    value = upgrader.upgrade('gene', gene_v4, current_version='4', target_version='5')
    assert annotation == value['transcriptome_annotation']
    assert 'annotation_version' not in value
    assert 'transcriptome_annotation' in value
    assert value['schema_version'] == '5'
