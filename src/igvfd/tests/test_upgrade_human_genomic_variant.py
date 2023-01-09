import pytest


def test_human_genomic_variant_upgrade_1_2(upgrader, human_genomic_variant_v1):
    alias = human_genomic_variant_v1['aliases']
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert value['schema_version'] == '2'
