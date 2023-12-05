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
