import pytest


def test_assay_term_upgrade_1_2(upgrader, platform_term_v1):
    value = upgrader.upgrade('platform_term', platform_term_v1, current_version='1', target_version='2')
    assert 'description' not in value
    assert value['schema_version'] == '2'
