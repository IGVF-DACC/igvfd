import pytest


def test_tabular_file_upgrade_1_2(upgrader, tabular_file_v1):
    value = upgrader.upgrade('tabular_file', tabular_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_tabular_file_upgrade_2_3(upgrader, tabular_file_v2):
    value = upgrader.upgrade('tabular_file', tabular_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_tabular_file_upgrade_3_4(upgrader, tabular_file_v3):
    value = upgrader.upgrade('tabular_file', tabular_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_tabular_file_upgrade_4_5(upgrader, tabular_file_v4):
    value = upgrader.upgrade('tabular_file', tabular_file_v4, current_version='4', target_version='5')
    assert 'assembly' in value
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '5'


def test_tabular_file_upgrade_5_6(upgrader, tabular_file_v5):
    value = upgrader.upgrade('tabular_file', tabular_file_v5, current_version='5', target_version='6')
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '6'


def test_tabular_file_upgrade_7_8(upgrader, tabular_file_v7):
    value = upgrader.upgrade('tabular_file', tabular_file_v7, current_version='7', target_version='8')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '8'


def test_tabular_file_upgrade_10_11(upgrader, tabular_file_v10):
    value = upgrader.upgrade('tabular_file', tabular_file_v10, current_version='10', target_version='11')
    assert value['content_type'] == 'fold change over control'
    assert value['schema_version'] == '11'


def test_tabular_file_upgrade_11_12(upgrader, tabular_file_v11):
    value = upgrader.upgrade('tabular_file', tabular_file_v11, current_version='11', target_version='12')
    assert value['content_type'] == 'variant effects'
    assert value['schema_version'] == '12'


def test_tabular_file_upgrade_12_13(upgrader, tabular_file_v12):
    value = upgrader.upgrade('tabular_file', tabular_file_v12, current_version='12', target_version='13')
    assert value['file_format'] == 'tsv'
    assert value['schema_version'] == '13'


def test_tabular_file_upgrade_14_15(upgrader, tabular_file_v14):
    value = upgrader.upgrade('tabular_file', tabular_file_v14, current_version='14', target_version='15')
    assert value['content_type'] == 'barcode onlist'
    assert value['schema_version'] == '15'


def test_tabular_file_upgrade_16_17_1(upgrader, tabular_file_v16_1):
    value = upgrader.upgrade('tabular_file', tabular_file_v15_1, current_version='16', target_version='17')
    assert value['content_type'] == 'variant functions'
    assert value['schema_version'] == '16'


def test_tabular_file_upgrade_16_17_2(upgrader, tabular_file_v16_2):
    value = upgrader.upgrade('tabular_file', tabular_file_v15_2, current_version='16', target_version='17')
    assert value['content_type'] == 'element to gene interactions'
    assert value['schema_version'] == '17'
