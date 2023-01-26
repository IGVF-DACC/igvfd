import pytest


def test_technical_sample_upgrade_1_2(upgrader, technical_sample_v1):
    value = upgrader.upgrade('technical_sample', technical_sample_v1, current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert 'aliases' not in value
    assert 'alternate_accessions' not in value
    assert value['schema_version'] == '2'


def test_technical_sample_upgrade_2_3(upgrader, technical_sample_v2):
    value = upgrader.upgrade('technical_sample', technical_sample_v2, current_version='2', target_version='3')
    assert 'additional_description' not in value
    assert value['description'] == 'This is a description.'
    assert value['schema_version'] == '3'


def test_technical_sample_upgrade_3_4(upgrader, technical_sample_v3):
    value = upgrader.upgrade('technical_sample', technical_sample_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'


def test_technical_sample_upgrade_4_5(upgrader, technical_sample_v4):
    value = upgrader.upgrade('technical_sample', technical_sample_v4, current_version='4', target_version='5')
    assert value['accession'] == 'IGVFBS0111TTTA'
    assert value['schema_version'] == '5'
