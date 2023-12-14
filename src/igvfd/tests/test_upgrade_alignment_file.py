import pytest


def test_alignment_file_upgrade_1_2(upgrader, alignment_file_v1):
    value = upgrader.upgrade('alignment_file', alignment_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_alignment_file_upgrade_2_3(upgrader, alignment_file_v2):
    value = upgrader.upgrade('alignment_file', alignment_file_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_alignment_file_upgrade_3_4(upgrader, alignment_file_v3):
    value = upgrader.upgrade('alignment_file', alignment_file_v3, current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_alignment_file_upgrade_4_5(upgrader, alignment_file_v4):
    value = upgrader.upgrade('alignment_file', alignment_file_v4, current_version='4', target_version='5')
    assert 'assembly' in value
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '5'
