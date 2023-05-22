import pytest


def test_biomarker_upgrade_1_2(upgrader, biomarker_v1):
    value = upgrader.upgrade('biomarker', biomarker_v1, current_version='1', target_version='2')
    assert value['status'] == 'in progress'
    assert value['schema_version'] == '2'
