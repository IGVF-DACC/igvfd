import pytest


def test_phenotypic_feature_upgrade_3_4(upgrader, phenotypic_feature_v1):
    value = upgrader.upgrade('phenotypic_feature', phenotypic_feature_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'description' not in value
