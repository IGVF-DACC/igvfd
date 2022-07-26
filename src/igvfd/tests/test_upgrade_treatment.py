import pytest


def test_treatment_upgrade_1_2(upgrader, treatment_version_v1):
    value = upgrader.upgrade('treatment', treatment_version_v1, current_version='1', target_version='2')
    assert 'documents' not in value
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
