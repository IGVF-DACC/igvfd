import pytest


def test_phenotype_term_upgrade_1_2(upgrader, phenotype_term_v1):
    value = upgrader.upgrade('phenotype_term', phenotype_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'


def test_phenotype_term_upgrade_2_3(upgrader, phenotype_term_v2):
    value = upgrader.upgrade('phenotype_term', phenotype_term_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_phenotype_term_upgrade_4_5(upgrader, phenotype_term_v4):
    value = upgrader.upgrade('phenotype_term', phenotype_term_v4, current_version='4', target_version='5')
    assert 'definition' not in value
    assert 'comment' not in value
    assert value['schema_version'] == '5'
