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
    expectation = sorted([
        'Histone ChIP-seq',
        'Parse SPLiT-seq',
        'SGE',
        'SHARE-seq',
        'Y2H',
        'Cell painting'
    ])
    value = upgrader.upgrade(
        'assay_term',
        assay_term_v3,
        current_version='3',
        target_version='4'
    )
    assert value['schema_version'] == '4'
    assert sorted(value['preferred_assay_titles']) == expectation


def test_assay_term_upgrade_5_6(upgrader, assay_term_v5):
    value = upgrader.upgrade('assay_term', assay_term_v5, current_version='5', target_version='6')
    assert 'preferred_assay_titles' not in value
    assert value['schema_version'] == '6'


def test_assay_term_upgrade_6_7(upgrader, assay_term_v6):
    value = upgrader.upgrade('assay_term', assay_term_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert set(value.get('preferred_assay_titles')) == {'CRISPR FlowFISH screen', 'Variant FlowFISH'}
