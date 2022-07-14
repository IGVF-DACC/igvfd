import pytest


def test_differentiated_cell_upgrade2(upgrader, differentiated_cell_1):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_1, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_differentiated_cell_upgrade1(upgrader, differentiated_cell_1):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
