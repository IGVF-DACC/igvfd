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
    assert 'dimension1' not in value
    assert 'dimension2' not in value
    assert value['schema_version'] == '7'
    assert value['principal_dimension'] == 'cell'
    assert value['secondary_dimensions'] == ['gene']


def test_matrix_file_upgrade_7_8(upgrader, matrix_file_v7):
    value = upgrader.upgrade('matrix_file', matrix_file_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['content_type'] == 'kallisto single cell RNAseq output'


def test_matrix_file_upgrade_9_10(upgrader, matrix_file_v9a, matrix_file_v9b, matrix_file_v9c, matrix_file_v9d):
    value = upgrader.upgrade('matrix_file', matrix_file_v9a, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['content_type'] == 'cell by gene matrix'
    assert value['filtered'] == False
    assert value['notes'].endswith(
        'This cell by gene sparse gene count matrix file was upgraded to cell by gene matrix.')

    value = upgrader.upgrade('matrix_file', matrix_file_v9b, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['content_type'] == 'cell by gene matrix'
    assert value['filtered'] == True
    assert value['notes'].endswith(
        'This cell by gene sparse gene count matrix file was upgraded to filtered cell by gene matrix.')

    value = upgrader.upgrade('matrix_file', matrix_file_v9c, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['content_type'] == 'cell by gene and peak matrix'
    assert value['filtered'] == True
    assert value['notes'].endswith(
        'This cell by gene expression, peak filtered feature barcode matrix file was upgraded to filtered cell by gene and peak matrix.')

    value = upgrader.upgrade('matrix_file', matrix_file_v9d, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['content_type'] == 'spot by gene matrix'
    assert value['notes'].endswith(
        'This time by peak contact matrix file did not match any combination in the upgrade logic and has been upgraded to spot by gene matrix as a placeholder.')
