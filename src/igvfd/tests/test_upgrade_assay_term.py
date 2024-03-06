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
    assert 'Histone ChIP-seq' in value['preferred_assay_titles']
    assert 'Parse SPLiT-seq' in value['preferred_assay_titles']
    assert 'SGE' in value['preferred_assay_titles']
    assert 'SHARE-seq' in value['preferred_assay_titles']
    assert 'Y2H' in value['preferred_assay_titles']
    assert 'Cell painting' in value['preferred_assay_titles']
    assert value['schema_version'] == '4'
