import pytest


def test_sample_term_upgrade_1_2(upgrader, sample_term_v1):
    value = upgrader.upgrade('sample_term', sample_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
