import pytest


def test_cell_line_upgrade_1_2(upgrader, cell_line_v1):
    value = upgrader.upgrade('cell_line', cell_line_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_cell_line_upgrade_2_3(upgrader, cell_line_v2):
    value = upgrader.upgrade('cell_line', cell_line_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_cell_line_upgrade_3_4(upgrader, cell_line_v3):
    value = upgrader.upgrade('cell_line', cell_line_v3, current_version='3', target_version='4')
    assert 'aliases' not in value
    assert 'donors' not in value
    assert 'dbxrefs' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'treatments' not in value
    assert value['schema_version'] == '4'
