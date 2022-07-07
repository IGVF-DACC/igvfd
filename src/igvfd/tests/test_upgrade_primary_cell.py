import pytest


def test_primary_cell_upgrade1(upgrader, primary_cell_1):
    value = upgrader.upgrade('primary_cell', primary_cell_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
