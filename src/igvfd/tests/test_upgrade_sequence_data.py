import pytest


def test_sequence_data_upgrade_1_2(upgrader, sequence_data_v1):
    value = upgrader.upgrade('curated_set', sequence_data_v1, current_version='1', target_version='2')
    assert value['accession'].startswith('IGVFFI')
    assert value['schema_version'] == '2'
