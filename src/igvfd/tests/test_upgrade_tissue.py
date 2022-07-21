import pytest


def test_tissue_upgrade_1_2(upgrader, tissue_1):
    value = upgrader.upgrade('tissue', tissue_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_tissue_upgrade_2_3(upgrader, tissue_2):
    value = upgrader.upgrade('tissue', tissue_2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_tissue_upgrade_3_4(upgrader, tissue_3):
    value = upgrader.upgrade('tissue', tissue_3, current_version='3', target_version='4')
    assert 'donors' not in value
    assert value['schema_version'] == '4'
