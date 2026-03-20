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
    value = upgrader.upgrade('tabular_file', tabular_file_v16_1, current_version='16', target_version='17')
    assert value['content_type'] == 'variant functions'
    assert value['schema_version'] == '17'


def test_tabular_file_upgrade_16_17_2(upgrader, tabular_file_v16_2):
    value = upgrader.upgrade('tabular_file', tabular_file_v16_2, current_version='16', target_version='17')
    assert value['content_type'] == 'element to gene interactions'
    assert value['schema_version'] == '17'


def test_tabular_file_upgrade_17_18(upgrader, tabular_file_v17):
    value = upgrader.upgrade('tabular_file', tabular_file_v17, current_version='17', target_version='18')
    assert value['content_type'] == 'pipeline parameters'
    assert value['schema_version'] == '18'


def test_tabular_file_upgrade_18_19(upgrader, tabular_file_v18a, tabular_file_v18b, tabular_file_v18c):
    value = upgrader.upgrade('tabular_file', tabular_file_v18a, current_version='18', target_version='19')
    assert value['content_type'] == 'global differential expression'
    assert value['filtered'] == True
    assert value['schema_version'] == '19'
    value = upgrader.upgrade('tabular_file', tabular_file_v18b, current_version='18', target_version='19')
    assert value['content_type'] == 'global differential expression'
    assert value['filtered'] == True
    assert value['schema_version'] == '19'
    value = upgrader.upgrade('tabular_file', tabular_file_v18c, current_version='18', target_version='19')
    assert value['content_type'] == 'local differential expression'
    assert value['filtered'] == False
    assert value['schema_version'] == '19'


def test_tabular_file_upgrade_20_21(upgrader, tabular_file_v20a, tabular_file_v20b, tabular_file_v20c, tabular_file_v20d, tabular_file_v20e):
    # A tabular file with submitted assembly.
    value = upgrader.upgrade('tabular_file', tabular_file_v20a, current_version='20', target_version='21')
    assert 'assembly' not in value
    assert 'submitted_assembly' in value
    assert value['submitted_assembly'] == 'GRCh38'
    assert 'The submitted assembly GRCh38 was moved to the submitted_assembly property.' in value['notes']
    assert value['schema_version'] == '21'
    # A tabular file with no assembly or reference_files.
    value = upgrader.upgrade('tabular_file', tabular_file_v20b, current_version='20', target_version='21')
    assert 'assembly' not in value
    assert 'submitted_assembly' in value
    assert value['submitted_assembly'] == 'unknown'
    assert 'This file\'s submitted_assembly was automatically set to unknown because the file had no assembly nor reference_files.' in value[
        'notes']
    assert value['schema_version'] == '21'
    # An excluded tabular file.
    value = upgrader.upgrade('tabular_file', tabular_file_v20c, current_version='20', target_version='21')
    assert value['schema_version'] == '21'
    # A tabular file with reference_files.
    value = upgrader.upgrade('tabular_file', tabular_file_v20d, current_version='20', target_version='21')
    assert value['schema_version'] == '21'
    # A deleted tabular file with no assembly or reference_files.
    value = upgrader.upgrade('tabular_file', tabular_file_v20e, current_version='20', target_version='21')
    assert value['reference_files'] == ['IGVFFI0653VCGH']
    assert 'This deleted file was automatically upgraded to add a link to IGVFFI0653VCGH in reference_files.' in value[
        'notes']
    assert value['schema_version'] == '21'
