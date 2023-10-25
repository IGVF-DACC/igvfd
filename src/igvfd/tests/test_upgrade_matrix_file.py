import pytest


def test_matrix_file_upgrade_1_2(upgrader, matrix_file_v1):
    value = upgrader.upgrade('matrix_file', matrix_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '5'
