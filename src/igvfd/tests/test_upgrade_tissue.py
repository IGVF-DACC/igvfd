import pytest


def test_tissue_upgrade1(upgrader, tissue_1):
    value = upgrader.upgrade('tissue', tissue_1, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_tissue_upgrade1(upgrader, tissue_1):
    value = upgrader.upgrade('tissue', tissue_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
