import pytest


def test_sample_term_upgrade_1_2(upgrader, sample_term_v1):
    value = upgrader.upgrade('sample_term', sample_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_sample_term_upgrade_2_3(upgrader, sample_term_v2):
    alias = sample_term_v2['aliases']
    deprecated_ntr_term = sample_term_v2['deprecated_ntr_terms']
    dbxref = sample_term_v2['dbxrefs']
    value = upgrader.upgrade('sample_term', sample_term_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'deprecated_ntr_terms' not in value
    assert deprecated_ntr_term == value['deprecated_ntr_term']
    assert 'dbxrefs' not in value
    assert dbxref == value['dbxref']
    assert value['schema_version'] == '3'
