import pytest


def test_biomarker_upgrade_1_2(upgrader, biomarker_v1):
    value = upgrader.upgrade('biomarker', biomarker_v1, current_version='1', target_version='2')
    assert value['status'] == 'in progress'
    assert value['schema_version'] == '2'


def test_biomarker_upgrade_2_3(upgrader, biomarker_v2):
    value = upgrader.upgrade('biomarker', biomarker_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'
