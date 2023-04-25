import pytest


def test_sequence_data_upgrade_1_2(upgrader, sequence_data_v1):
    value = upgrader.upgrade('sequence_data', sequence_data_v1, current_version='1', target_version='2')
    assert value['accession'] == 'IGVFFI0999AAAA'
    assert value['schema_version'] == '2'


def test_sequence_data_upgrade_2_3(upgrader, sequence_data_v2):
    value = upgrader.upgrade('sequence_data', sequence_data_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
