import pytest


def test_sequence_file_upgrade_2_3(upgrader, sequence_file_v2):
    value = upgrader.upgrade('sequence_file', sequence_file_v2, current_version='2', target_version='3')
    assert value['sequencing_platform'] == '/platform-terms/EFO_0004203/'
    assert value['schema_version'] == '3'


def test_sequence_file_upgrade_3_4(upgrader, sequence_file_v3):
    value = upgrader.upgrade('sequence_file', sequence_file_v3, current_version='3', target_version='4')
    assert value['maximum_read_length'] == 300000000
    assert value['minimum_read_length'] == 300000000
    assert value['mean_read_length'] == 300000000
    assert value['schema_version'] == '4'


def test_sequence_file_upgrade_4_5(upgrader, sequence_file_v4):
    value = upgrader.upgrade('sequence_file', sequence_file_v4, current_version='4', target_version='5')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '5'


def test_sequence_file_upgrade_5_6(upgrader, sequence_file_v5):
    value = upgrader.upgrade('sequence_file', sequence_file_v5, current_version='5', target_version='6')
    assert 'description' not in value
    assert value['schema_version'] == '6'


def test_sequence_file_upgrade_6_7(upgrader, sequence_file_v6):
    value = upgrader.upgrade('sequence_file', sequence_file_v6, current_version='6', target_version='7')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '7'


def test_sequence_file_upgrade_7_8(upgrader, sequence_file_v7_v1, sequence_file_v7_v2, sequence_file_v7_v3):
    value = upgrader.upgrade('sequence_file', sequence_file_v7_v1, current_version='7', target_version='8')
    assert value['content_type'] == 'PacBio subreads'
    assert value['schema_version'] == '8'
    value = upgrader.upgrade('sequence_file', sequence_file_v7_v2, current_version='7', target_version='8')
    assert value['content_type'] == 'PacBio subreads'
    assert value['schema_version'] == '8'
    value = upgrader.upgrade('sequence_file', sequence_file_v7_v3, current_version='7', target_version='8')
    assert value['content_type'] == 'reads'
    assert value['schema_version'] == '8'


def test_sequence_file_upgrade_8_9(upgrader, sequence_file_v8):
    value = upgrader.upgrade('sequence_file', sequence_file_v8, current_version='8', target_version='9')
    assert 'seqspec' not in value
    assert value['schema_version'] == '9'


def test_sequence_file_upgrade_9_10(upgrader, sequence_file_v9):
    value = upgrader.upgrade('sequence_file', sequence_file_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['release_timestamp'] == '2024-03-06T12:34:56Z'
    assert value['notes'] == 'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'


def test_sequence_file_upgrade_10_11(upgrader, sequence_file_v10):
    value = upgrader.upgrade('sequence_file', sequence_file_v10, current_version='10', target_version='11')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '11'


def test_sequence_file_upgrade_10_11(upgrader, sequence_file_v10):
    value = upgrader.upgrade('sequence_file', sequence_file_v10, current_version='10', target_version='11')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '11'


def test_sequence_file_upgrade_12_13(upgrader, sequence_file_v12):
    value = upgrader.upgrade('sequence_file', sequence_file_v12, current_version='12', target_version='13')
    assert value['sequencing_kit'] == 'NovaSeq 6000 S4 Reagent Kit v1.5'
    assert value['schema_version'] == '13'
