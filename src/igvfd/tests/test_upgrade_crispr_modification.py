import pytest


def test_crispr_modification_upgrade_1_2(upgrader, crispr_modification_v1_krab, crispr_modification_v1_zim3):
    value = upgrader.upgrade('crispr_modification', crispr_modification_v1_krab,
                             current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'fused_domain' not in value
    assert value['notes'].endswith('removed.')
    value = upgrader.upgrade('crispr_modification', crispr_modification_v1_zim3,
                             current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert value['fused_domain'] == 'ZIM3-KRAB'
    assert value['notes'].endswith('renamed to be ZIM3-KRAB.')
