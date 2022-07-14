import pytest


def test_cell_line_upgrade2(upgrader, cell_line_1):
    value = upgrader.upgrade('cell_line', cell_line_1, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_cell_line_upgrade1(upgrader, cell_line_1):
    value = upgrader.upgrade('cell_line', cell_line_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
