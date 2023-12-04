import pytest


def test_sample_term_upgrade_1_2(upgrader, sample_term_v1):
    value = upgrader.upgrade('sample_term', sample_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_sample_term_upgrade_2_3(upgrader, sample_term_v2):
    value = upgrader.upgrade('sample_term', sample_term_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'
