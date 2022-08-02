import pytest


def test_phenotype_term_upgrade_1_2(upgrader, phenotype_term_v1):
    value = upgrader.upgrade('phenotype_term', phenotype_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
