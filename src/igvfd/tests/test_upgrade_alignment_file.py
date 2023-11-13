import pytest


def test_alignment_file_upgrade_1_2(upgrader, alignment_file_v1):
    value = upgrader.upgrade('alignment_file', alignment_file_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'
