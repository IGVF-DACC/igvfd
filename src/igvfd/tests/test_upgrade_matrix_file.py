import pytest


def test_matrix_file_upgrade_1_2(upgrader, matrix_file_v1):
    value = upgrader.upgrade('matrix_file', matrix_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_matrix_file_upgrade_2_3(upgrader, matrix_file_v2):
    value = upgrader.upgrade('matrix_file', matrix_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_matrix_file_upgrade_3_4(upgrader, matrix_file_v3):
    value = upgrader.upgrade('matrix_file', matrix_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_matrix_file_upgrade_5_6(upgrader, matrix_file_v5):
    value = upgrader.upgrade('matrix_file', matrix_file_v5, current_version='5', target_version='6')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '6'


def test_matrix_file_upgrade_6_7(upgrader, matrix_file_v6):
    value = upgrader.upgrade('matrix_file', matrix_file_v6, current_version='6', target_version='7')
    assert 'principal_dimension' not in value
    assert 'secondary_dimensions' not in value
    assert value['schema_version'] == '7'
    assert value['principal_dimension'] == 'cell'
    assert value['secondary_dimensions'] == ['gene']
