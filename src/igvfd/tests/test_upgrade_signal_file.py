import pytest


def test_signal_file_upgrade_1_2(upgrader, signal_file_v1):
    value = upgrader.upgrade('signal_file', signal_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_signal_file_upgrade_2_3(upgrader, signal_file_v2):
    value = upgrader.upgrade('signal_file', signal_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_signal_file_upgrade_3_4(upgrader, signal_file_v3):
    value = upgrader.upgrade('signal_file', signal_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_signal_file_upgrade_4_5(upgrader, signal_file_v4):
    value = upgrader.upgrade('signal_file', signal_file_v4, current_version='4', target_version='5')
    assert 'assembly' in value
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '5'


def test_signal_file_upgrade_5_6(upgrader, signal_file_v5):
    value = upgrader.upgrade('signal_file', signal_file_v5, current_version='5', target_version='6')
    assert value['assembly'] == 'GRCm39'
    assert value['schema_version'] == '6'


def test_signal_file_upgrade_7_8(upgrader, signal_file_v7):
    value = upgrader.upgrade('signal_file', signal_file_v7, current_version='7', target_version='8')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '8'


def test_signal_file_upgrade_8_9(upgrader, signal_file_v8):
    value = upgrader.upgrade('signal_file', signal_file_v8, current_version='8', target_version='9')
    assert value['content_type'] == 'fold change over control'
    assert value['schema_version'] == '9'


def test_signal_file_upgrade_10_11(upgrader, signal_file_v10, registry):
    value = upgrader.upgrade('alignment_file', signal_file_v10, current_version='10',
                             target_version='11', registry=registry)
    assert value['schema_version'] == '11'
    assert value['derived_manually'] == False
    assert value['normalized'] == False
