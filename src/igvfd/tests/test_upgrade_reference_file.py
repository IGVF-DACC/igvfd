import pytest


def test_reference_file_upgrade_2_3(upgrader, reference_file_v2):
    value = upgrader.upgrade('reference_file', reference_file_v2, current_version='2', target_version='3')
    assert reference_file_v2['source'] == value['source_url']
    assert 'source' not in value
    assert 'source_url' in value
    assert value['schema_version'] == '3'
