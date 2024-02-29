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
