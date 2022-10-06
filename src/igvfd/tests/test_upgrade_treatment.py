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
