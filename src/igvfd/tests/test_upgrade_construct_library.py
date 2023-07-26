import pytest


def test_construct_library_upgrade_1_2(upgrader, construct_library_v1):
    value = upgrader.upgrade(
        'construct_library', construct_library_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'plasmid_map' not in value
    assert (len(construct_library_v1['documents'])) == 2


def test_construct_library_upgrade_2_3(upgrader, construct_library_v2):
    value = upgrader.upgrade(
        'construct_library', construct_library_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'origins' in value
    assert 'guide_library_details' in value


def test_construct_library_upgrade_3_4(upgrader, construct_library_v3):
    selection_criteria = construct_library_v3['origins']
    value = upgrader.upgrade('construct_library', construct_library_v3, current_version='3', target_version='4')
    assert 'origins' not in value
    assert selection_criteria == value['selection_criteria']
    assert value['schema_version'] == '4'


def test_construct_library_upgrade_4_5(upgrader, construct_library_v4):
    value = upgrader.upgrade(
        'construct_library', construct_library_v4,
        current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'publication_identifiers' in value
    assert 'references' not in value
