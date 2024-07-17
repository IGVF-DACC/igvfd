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


def test_crispr_modification_upgrade_2_3(upgrader, crispr_modification_v2):
    value = upgrader.upgrade('crispr_modification', crispr_modification_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'product_id' not in value
    assert 'lot_id' not in value
    assert 'notes' in value and value['notes'].endswith(
        'Product_id 100A was removed from this modification. Lot_id 123 was removed from this modification.')
