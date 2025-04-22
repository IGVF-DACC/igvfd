import pytest


def test_sample_term_upgrade_1_2(upgrader, sample_term_v1):
    value = upgrader.upgrade('sample_term', sample_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_sample_term_upgrade_2_3(upgrader, sample_term_v2):
    value = upgrader.upgrade('sample_term', sample_term_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_sample_term_upgrade_4_5(upgrader, sample_term_v4):
    value = upgrader.upgrade('sample_term', sample_term_v4, current_version='4', target_version='5')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '5'


def test_sample_term_upgrade_5_6(upgrader, sample_term_v5):
    value = upgrader.upgrade('sample_term', sample_term_v5, current_version='5', target_version='6')
    assert 'definition' not in value
    assert 'comment' not in value
    assert value['schema_version'] == '6'
