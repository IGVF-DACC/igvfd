import pytest


def test_assay_term_upgrade_1_2(upgrader, assay_term_v1):
    value = upgrader.upgrade('assay_term', assay_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_assay_term_upgrade_2_3(upgrader, assay_term_v2):
    value = upgrader.upgrade('assay_term', assay_term_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_assay_term_upgrade_3_4(upgrader, assay_term_v3):
    value = upgrader.upgrade('assay_term', assay_term_v3, current_version='3', target_version='4')
    assert 'preferred_assay_titles' in value
    assert value['preferred_assay_titles'] == 'Parse SPLiT-seq'
    assert value['schema_version'] == '4'
