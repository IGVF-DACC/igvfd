import pytest


def test_prediction_set_upgrade_1_2(upgrader, prediction_set_v1):
    value = upgrader.upgrade('prediction_set', prediction_set_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_prediction_set_upgrade_2_3(upgrader, prediction_set_v2):
    value = upgrader.upgrade('prediction_set', prediction_set_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value


def test_prediction_set_upgrade_3_4(upgrader, prediction_set_v3):
    original_loci = prediction_set_v3['targeted_loci']
    original_genes = prediction_set_v3['targeted_genes']
    value = upgrader.upgrade('prediction_set', prediction_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'loci' in value and 'targeted_loci' not in value and value['loci'] == original_loci
    assert 'genes' in value and 'targeted_genes' not in value and value['genes'] == original_genes


def test_prediction_set_set_upgrade_4_5(upgrader, prediction_set_v4):
    genes = prediction_set_v4['genes']
    value = upgrader.upgrade('prediction_set', prediction_set_v4, current_version='4', target_version='5')
    assert 'genes' not in value and value['small_scale_gene_list'] == genes
    assert value['schema_version'] == '5'


def test_prediction_set_set_upgrade_5_6(upgrader, prediction_set_v5):
    value = upgrader.upgrade('prediction_set', prediction_set_v5, current_version='5', target_version='6')
    for loci in value['small_scale_loci_list']:
        assert loci['assembly'] == 'GRCh38'
    assert value['schema_version'] == '6'


def test_prediction_set_set_upgrade_7_8(upgrader, prediction_set_v7):
    value = upgrader.upgrade('prediction_set', prediction_set_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert 'publication_identifiers' not in value


def test_prediction_set_set_upgrade_8_9(upgrader, prediction_set_v8):
    value = upgrader.upgrade('prediction_set', prediction_set_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert value['file_set_type'] == 'functional effect'
