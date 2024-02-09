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
    value = upgrader.upgrade('prediction_set', prediction_set_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
