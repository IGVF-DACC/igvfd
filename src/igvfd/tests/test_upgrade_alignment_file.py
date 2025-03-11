import pytest


def test_alignment_file_upgrade_1_2(upgrader, alignment_file_v1):
    value = upgrader.upgrade('alignment_file', alignment_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_alignment_file_upgrade_2_3(upgrader, alignment_file_v2):
    value = upgrader.upgrade('alignment_file', alignment_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_alignment_file_upgrade_3_4(upgrader, alignment_file_v3):
    value = upgrader.upgrade('alignment_file', alignment_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_alignment_file_upgrade_4_5(upgrader, alignment_file_v4):
    value = upgrader.upgrade('alignment_file', alignment_file_v4, current_version='4', target_version='5')
    assert 'assembly' in value
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '5'


def test_alignment_file_upgrade_5_6(upgrader, alignment_file_v5):
    value = upgrader.upgrade('alignment_file', alignment_file_v5, current_version='5', target_version='6')
    assert value['assembly'] == 'GRCm39'
    assert value['schema_version'] == '6'


def test_alignment_file_upgrade_7_8(upgrader, alignment_file_v7):
    value = upgrader.upgrade('alignment_file', alignment_file_v7, current_version='7', target_version='8')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '8'


def test_alignment_file_upgrade_8_9(upgrader, alignment_file_v8):
    value = upgrader.upgrade('alignment_file', alignment_file_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'


def test_alignment_file_upgrade_9_10(upgrader, alignment_file_v9):
    assert 'anvil_source_url' in alignment_file_v9
    assert 'release_timestamp' in alignment_file_v9
    assert alignment_file_v9['controlled_access'] is True
    assert alignment_file_v9['upload_status'] == 'deposited'
    assert alignment_file_v9['status'] == 'released'
    value = upgrader.upgrade('alignment_file', alignment_file_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert 'anvil_source_url' not in value
    assert 'release_timestamp' not in value
    assert alignment_file_v9['upload_status'] == 'pending'
    assert value['controlled_access'] is True
    assert value['status'] == 'in progress'


def test_alignment_file_upgrade_10_11(upgrader, alignment_file_v10):
    value = upgrader.upgrade('alignment_file', alignment_file_v10, current_version='10', target_version='11')
    assert alignment_file_v10['file_format'] == 'bam'
    assert alignment_file_v10['notes'].endswith('but has been upgraded to .bam.')
    assert alignment_file_v10['schema_version'] == '11'


def test_alignment_file_upgrade_11_12(upgrader, alignment_file_v11):
    value = upgrader.upgrade('alignment_file', alignment_file_v11, current_version='11', target_version='12')
    assert 'assembly' in value
    assert alignment_file_v11['assembly'] == 'custom'
    assert alignment_file_v11['notes'].endswith('has been assigneed to be custom via an upgrade.')
    assert alignment_file_v11['schema_version'] == '12'


def test_alignment_file_upgrade_12_13(upgrader, alignment_file_v12):
    assert alignment_file_v12['read_count'] == 23040138.0
    value = upgrader.upgrade('alignment_file', alignment_file_v12, current_version='12', target_version='13')
    assert alignment_file_v12['read_count'] == 23040138
    assert alignment_file_v12['schema_version'] == '13'


def test_alignment_file_upgrade_13_14(upgrader, alignment_file_v13):
    value = upgrader.upgrade('alignment_file', alignment_file_v13, current_version='13', target_version='14')
    assert value['schema_version'] == '14'
    assert set(value.get('transcriptome_annotation')) == 'GENCODE 32, GENCODE M23'
