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


def test_assay_term_upgrade_7_8(upgrader, assay_term_v7):
    value = upgrader.upgrade('assay_term', assay_term_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert set(value.get('preferred_assay_titles')) == {'Variant painting via fluorescence'}


def test_assay_term_upgrade_8_9(upgrader, assay_term_v8):
    value = upgrader.upgrade('assay_term', assay_term_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert set(value.get('preferred_assay_titles')) == {'Variant-EFFECTS'}


def test_assay_term_upgrade_9_10(upgrader, assay_term_v9):
    value = upgrader.upgrade('assay_term', assay_term_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert set(value.get('preferred_assay_titles')) == {'10x multiome with scMito-seq'}


def test_assay_term_upgrade_10_11(upgrader, assay_term_v10):
    value = upgrader.upgrade('assay_term', assay_term_v10, current_version='10', target_version='11')
    assert value['schema_version'] == '11'
    assert set(value.get('preferred_assay_titles')) == {'Proliferation CRISPR screen'}


def test_assay_term_upgrade_11_12(upgrader, assay_term_v11):
    value = upgrader.upgrade('assay_term', assay_term_v11, current_version='11', target_version='12')
    assert 'definition' not in value
    assert 'comment' not in value
    assert value['schema_version'] == '12'


def test_assay_term_upgrade_12_13(upgrader, assay_term_v12):
    value = upgrader.upgrade('assay_term', assay_term_v12, current_version='12', target_version='13')
    assert 'SUPERSTARR' not in value['preferred_assay_titles'] and 'STARR-seq' in value['preferred_assay_titles']
    assert value['schema_version'] == '13'


def test_assay_term_upgrade_13_14(upgrader, assay_term_v13):
    value = upgrader.upgrade('assay_term', assay_term_v13, current_version='13', target_version='14')
    assert value['schema_version'] == '14'
    assert set(value.get('preferred_assay_titles')) == {'mtscMultiome'}


def test_assay_term_upgrade_14_15(upgrader, assay_term_v14):
    value = upgrader.upgrade('assay_term', assay_term_v14, current_version='14', target_version='15')
    assert value['schema_version'] == '15'
    assert 'preferred_assay_titles' not in value
