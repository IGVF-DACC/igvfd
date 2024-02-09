import pytest


def test_construct_library_set_upgrade_1_2(upgrader, construct_library_set_v1):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v1, current_version='1', target_version='2')
    assert value['exon'] == 'exon_ID'
    assert value['schema_version'] == '2'


def test_construct_library_set_upgrade_2_3(upgrader, construct_library_set_v2):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_construct_library_set_upgrade_3_4(upgrader, construct_library_set_v3):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'


def test_construct_library_set_upgrade_4_5(upgrader, construct_library_set_v4):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
