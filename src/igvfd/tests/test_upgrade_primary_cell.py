import pytest


def test_primary_cell_upgrade1(upgrader, primary_cell_2):
    value = upgrader.upgrade('primary_cell', primary_cell_2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_primary_cell_upgrade1(upgrader, primary_cell_1):
    value = upgrader.upgrade('primary_cell', primary_cell_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
