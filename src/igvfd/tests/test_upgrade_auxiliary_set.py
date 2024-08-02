import pytest


def test_auxiliary_set_upgrade_1_2(upgrader, auxiliary_set_v1):
    ids = auxiliary_set_v1['references']
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_auxiliary_set_upgrade_2_3(upgrader, auxiliary_set_v2):
    old_auxiliary_type = auxiliary_set_v2['auxiliary_type']
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'file_set_type' in value and value['file_set_type'] == old_auxiliary_type
    assert 'auxiliary_type' not in value


def test_auxiliary_set_upgrade_3_4(upgrader, auxiliary_set_v3):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v3,
        current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'construct_libraries' not in value
    assert 'moi' not in value


def test_auxiliary_set_upgrade_4_5(upgrader, auxiliary_set_v4):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v4,
        current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'description' not in value


def test_auxiliary_set_upgrade_5_6(upgrader, auxiliary_set_v5):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v5,
        current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['file_set_type'] == 'cell hashing'


def test_auxiliary_set_upgrade_7_8(upgrader, auxiliary_set_v7_circularized_barcode, auxiliary_set_v7_barcode_seq):
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v7_circularized_barcode,
        current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['file_set_type'] == 'circularized RNA barcode detection'
    value = upgrader.upgrade(
        'auxiliary_set', auxiliary_set_v7_barcode_seq,
        current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['file_set_type'] == 'quantification DNA barcode sequencing'


def test_auxiliary_set_upgrade_8_9(upgrader, auxiliary_set_v8):
    value = upgrader.upgrade('auxiliary_set', auxiliary_set_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'publication_identifiers' not in value


def test_auxiliary_set_upgrade_9_10(upgrader, auxiliary_set_v9):
    value = upgrader.upgrade('auxiliary_set', auxiliary_set_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert 'library_construction_platform' not in value
