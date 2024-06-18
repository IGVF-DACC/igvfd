import pytest


def test_crispr_modification_upgrade_1_2(upgrader, crispr_modification_v1):
    value = upgrader.upgrade('crispr_modification', crispr_modification_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert value['fused_doamin'] == 'ZIM3-KRAB'
