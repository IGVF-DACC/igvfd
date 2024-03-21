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


def test_gene_upgrade_5_6(upgrader, gene_v5):
    value = upgrader.upgrade('gene', gene_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert 'description' not in value


def test_gene_upgrade_6_7(upgrader, gene_v6):
    value = upgrader.upgrade('gene', gene_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    for location in value['locations']:
        assert location['assembly'] == 'GRCm39'


def test_gene_upgrade_8_9(upgrader, gene_v8):
    value = upgrader.upgrade('gene', gene_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'synonyms' not in value
