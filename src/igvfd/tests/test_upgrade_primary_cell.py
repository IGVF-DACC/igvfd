import pytest


def test_primary_cell_upgrade_1_2(upgrader, primary_cell_1):
    value = upgrader.upgrade('primary_cell', primary_cell_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_primary_cell_upgrade_2_3(upgrader, primary_cell_2):
    value = upgrader.upgrade('primary_cell', primary_cell_2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_primary_cell_upgrade_3_4(upgrader, primary_cell_3):
    value = upgrader.upgrade('primary_cell', primary_cell_3, current_version='3', target_version='4')
    assert 'alternate_accessions' not in value
    assert value['schema_version'] == '4'
