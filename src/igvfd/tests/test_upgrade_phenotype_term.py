import pytest


def test_phenotype_term_upgrade_1_2(upgrader, phenotype_term_v1):
    value = upgrader.upgrade('phenotype_term', phenotype_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_phenotype_term_upgrade_2_3(upgrader, phenotype_term_v2):
    alias = phenotype_term_v2['aliases']
    deprecated_ntr_term = phenotype_term_v2['deprecated_ntr_terms']
    value = upgrader.upgrade('phenotype_term', phenotype_term_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'deprecated_ntr_terms' not in value
    assert deprecated_ntr_term == value['deprecated_ntr_term']
    assert value['schema_version'] == '3'
