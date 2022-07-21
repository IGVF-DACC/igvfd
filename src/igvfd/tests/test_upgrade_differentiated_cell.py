import pytest


def test_differentiated_cell_upgrade_1_2(upgrader, differentiated_cell_1):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_differentiated_cell_upgrade_2_3(upgrader, differentiated_cell_2):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_differentiated_cell_upgrade_3_4(upgrader, differentiated_cell_3):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_3, current_version='3', target_version='4')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '4'


def test_differentiated_cell_upgrade_4_5(upgrader, differentiated_cell_4):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'post_differentiation_time' not in value
    assert 'post_differentiation_time_units' not in value


def test_differentiated_cell_upgrade_4_5_good_value(upgrader, differentiated_cell_4_good_value):
    value = upgrader.upgrade('differentiated_cell', differentiated_cell_4_good_value,
                             current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'post_differentiation_time' in value
    assert 'post_differentiation_time_units' in value