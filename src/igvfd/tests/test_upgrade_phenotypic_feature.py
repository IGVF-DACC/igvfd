import pytest


def test_phenotypic_feature_upgrade_1_2(upgrader, phenotypic_feature_v1):
    value = upgrader.upgrade('phenotypic_feature', phenotypic_feature_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'description' not in value


def test_phenotypic_feature_upgrade_3_4(upgrader, phenotypic_feature_v3):
    value = upgrader.upgrade('phenotypic_feature', phenotypic_feature_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert value['quality'] == 'E2/E2'
