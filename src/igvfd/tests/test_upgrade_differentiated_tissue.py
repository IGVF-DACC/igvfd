import pytest


def test_differentiated_tissue_upgrade1(upgrader, differentiated_tissue_2):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_differentiated_tissue_upgrade1(upgrader, differentiated_tissue_1):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
