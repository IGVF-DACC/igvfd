import pytest


def test_reference_data_upgrade_2_3(upgrader, reference_data_v2):
    value = upgrader.upgrade('sequence_data', reference_data_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
