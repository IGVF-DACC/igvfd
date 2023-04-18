import pytest


def test_construct_library_upgrade_1_2(upgrader, construct_library_v1):
    value = upgrader.upgrade(
        'construct_library', construct_library_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'plasmid_map' not in value
    assert (len(construct_library_v1['documents'])) == 2
