import pytest


def test_sequence_file_upgrade_2_3(upgrader, sequence_file_v2):
    value = upgrader.upgrade('sequence_file', sequence_file_v2, current_version='2', target_version='3')
    assert value['sequencing_platform'] == '/platform-terms/EFO_0004203/'
    assert value['schema_version'] == '3'


def test_sequence_file_upgrade_3_4(upgrader, sequence_file_v3):
    value = upgrader.upgrade('sequence_file', sequence_file_v3, current_version='3', target_version='4')
    assert value['max_read_length'] == 300000000
    assert value['min_read_length'] == 300000000
    assert value['mean_read_length'] == 300000000
    assert value['schema_version'] == '4'
