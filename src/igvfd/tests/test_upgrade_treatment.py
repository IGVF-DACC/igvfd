import pytest


def test_treatment_upgrade_1_2(upgrader, treatment_v1):
    value = upgrader.upgrade('treatment', treatment_v1, current_version='1', target_version='2')
    assert 'documents' not in value
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_treatment_upgrade_2_3(upgrader, treatment_v2):
    value = upgrader.upgrade('treatment', treatment_v2, current_version='2', target_version='3')
    assert value['notes'] == 'This treatment did not have purpose specified previously, it was upgraded to have perturbation purpose.'
    assert value['purpose'] == 'perturbation'
    assert value['schema_version'] == '3'


def test_treatment_upgrade_3_4(upgrader, treatment_v3):
    value = upgrader.upgrade('treatment', treatment_v3, current_version='3', target_version='4')
    assert value['notes'] == 'This treatment does not have award, lab, depletion specified previously, it was upgraded to have Cherry lab/award and depletion=False.'
    assert value['lab'] == '/labs/j-michael-cherry'
    assert value['award'] == '/awards/HG012012'
    assert value['depletion'] == False
    assert value['schema_version'] == '4'


def test_treatment_upgrade_4_5(upgrader, treatment_v4):
    sources = [treatment_v4['source']]
    value = upgrader.upgrade('treatment', treatment_v4, current_version='4', target_version='5')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert value['schema_version'] == '5'


def test_treatment_upgrade_5_6(upgrader, treatment_v5):
    value = upgrader.upgrade('treatment', treatment_v5, current_version='5', target_version='6')
    assert 'description' not in value
    assert value['schema_version'] == '6'


def test_treatment_upgrade_6_7(upgrader, treatment_v6):
    value = upgrader.upgrade('treatment', treatment_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert value['release_timestamp'] == '2024-03-06T12:34:56Z'
    assert value['notes'] == 'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'


def test_treatment_upgrade_7_8(upgrader, treatment_v7a, treatment_v7b):
    value = upgrader.upgrade('treatment', treatment_v7a, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert 'product_id' not in value
    assert 'lot_id' not in value
    assert 'notes' in value and value['notes'].endswith(
        'Product_id 100A was removed from this treatment. Lot_id 123 was removed from this treatment.')
    value = upgrader.upgrade('treatment', treatment_v7b, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert 'lot_id' not in value
    assert 'notes' in value and value['notes'].endswith(
        'Lot_id 123 was removed from this treatment.')
