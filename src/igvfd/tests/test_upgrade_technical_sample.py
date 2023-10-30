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
    assert value['accession'] == 'IGVFSM0111TTTA'
    assert value['schema_version'] == '5'


def test_technical_sample_upgrade_5_6(upgrader, technical_sample_v5):
    value = upgrader.upgrade('technical_sample', technical_sample_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['sorted_fraction_detail'] == 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


def test_technical_sample_upgrade_6_7(upgrader, technical_sample_v6):
    value = upgrader.upgrade('technical_sample', technical_sample_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert value['virtual'] == False


def test_technical_sample_upgrade_7_8(upgrader, technical_sample_v7):
    sources = [technical_sample_v7['source']]
    sample_terms = [technical_sample_v7['technical_sample_term']]
    modifications = [technical_sample_v7['modification']]
    value = upgrader.upgrade('technical_sample', technical_sample_v7, current_version='7', target_version='8')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert 'technical_sample_term' not in value
    assert sample_terms == value['sample_terms']
    assert type(value['sample_terms']) == list
    assert 'modification' not in value
    assert modifications == value['modifications']
    assert type(value['modifications']) == list
    assert value['schema_version'] == '8'


def test_technical_sample_8_9(upgrader, technical_sample_v8_no_units, technical_sample_v8_no_amount):
    value = upgrader.upgrade('technical_sample', technical_sample_v8_no_units, current_version='8', target_version='9')
    assert 'starting_amount_units' in value and value['starting_amount_units'] == 'items'
    assert value['schema_version'] == '9'
    value = upgrader.upgrade('technical_sample', technical_sample_v8_no_amount, current_version='8', target_version='9')
    assert 'starting_amount' in value and value['starting_amount'] == 0
    assert value['schema_version'] == '9'


def test_technical_sample_upgrade_9_10(upgrader, technical_sample_v9):
    sorted_sample = technical_sample_v9['sorted_fraction']
    sorted_sample_detail = technical_sample_v9['sorted_fraction_detail']
    value = upgrader.upgrade('technical_sample', technical_sample_v9, current_version='9', target_version='10')
    assert 'sorted_from' in value and value['sorted_from'] == sorted_sample
    assert 'sorted_from_detail' in value and value['sorted_from_detail'] == sorted_sample_detail
    assert value['schema_version'] == '10'
