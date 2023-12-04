import pytest


def test_primary_cell_upgrade_1_2(upgrader, primary_cell_v1):
    value = upgrader.upgrade('primary_cell', primary_cell_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_primary_cell_upgrade_2_3(upgrader, primary_cell_v2):
    value = upgrader.upgrade('primary_cell', primary_cell_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_primary_cell_upgrade_3_4(upgrader, primary_cell_v3):
    value = upgrader.upgrade('primary_cell', primary_cell_v3, current_version='3', target_version='4')
    assert 'aliases' not in value
    assert 'donors' not in value
    assert 'dbxrefs' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'treatments' not in value
    assert value['schema_version'] == '4'


def test_primary_cell_upgrade_4_5(upgrader, primary_cell_v4, phenotype_term_alzheimers):
    value = upgrader.upgrade('primary_cell', primary_cell_v4, current_version='4', target_version='5')
    assert 'disease_term' not in value
    assert value['schema_version'] == '5'
    assert value.get('disease_terms') == [phenotype_term_alzheimers['@id']]


def test_primary_cell_upgrade_5_6(upgrader, primary_cell_v5, primary_cell_v5_unknown, primary_cell_v5_90_or_above):
    value = upgrader.upgrade('primary_cell', primary_cell_v5, current_version='5', target_version='6')
    assert value['lower_bound_age'] == 10 and value['upper_bound_age'] == 10
    assert value['embryonic']
    assert 'life_stage' not in value
    assert value['schema_version'] == '6'
    value = upgrader.upgrade('primary_cell', primary_cell_v5_unknown, current_version='5', target_version='6')
    assert 'life_stage' not in value
    assert 'age' not in value
    assert value['schema_version'] == '6'
    value = upgrader.upgrade('primary_cell', primary_cell_v5_90_or_above, current_version='5', target_version='6')
    assert 'life_stage' not in value
    assert value['lower_bound_age'] == 90 and value['upper_bound_age'] == 90
    assert value['schema_version'] == '6'


def test_primary_cell_upgrade_6_7(upgrader, primary_cell_v6):
    assert 'donor' in primary_cell_v6
    value = upgrader.upgrade('primary_cell', primary_cell_v6, current_version='6', target_version='7')
    assert 'donor' not in value
    assert 'donors' in value
    assert value['schema_version'] == '7'


def test_primary_cell_upgrade_7_8(upgrader, primary_cell_v7):
    biomarkers = primary_cell_v7['biomarker']
    value = upgrader.upgrade('primary_cell', primary_cell_v7, current_version='7', target_version='8')
    assert 'biomarker' not in value
    assert biomarkers == value['biomarkers']
    assert value['schema_version'] == '8'


def test_primary_cell_upgrade_8_9(upgrader, primary_cell_v8):
    value = upgrader.upgrade('primary_cell', primary_cell_v8, current_version='8', target_version='9')
    assert value['accession'] == 'IGVFSM0666PPCA'
    assert value['schema_version'] == '9'


def test_primary_cell_upgrade_9_10(upgrader, primary_cell_v9):
    value = upgrader.upgrade('primary_cell', primary_cell_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['sorted_fraction_detail'] == 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


def test_primary_cell_upgrade_10_11(upgrader, primary_cell_v10):
    value = upgrader.upgrade('primary_cell', primary_cell_v10, current_version='10', target_version='11')
    assert value['schema_version'] == '11'
    assert value['taxa'] != 'Saccharomyces'
    assert value['notes'] == 'Previous taxa: Saccharomyces is no longer valid.'


def test_primary_cell_upgrade_11_12(upgrader, primary_cell_v11):
    value = upgrader.upgrade('primary_cell', primary_cell_v11, current_version='11', target_version='12')
    assert value['schema_version'] == '12'
    assert 'taxa' not in value
    assert value['notes'] == 'Previous taxa: Homo sapiens will now be calculated.'


def test_primary_cell_upgrade_12_13(upgrader, primary_cell_v12):
    value = upgrader.upgrade('primary_cell', primary_cell_v12, current_version='12', target_version='13')
    assert value['schema_version'] == '13'
    assert 'virtual' in value


def test_primary_cell_upgrade_13_14(upgrader, primary_cell_v13):
    sources = [primary_cell_v13['source']]
    sample_terms = [primary_cell_v13['biosample_term']]
    modifications = [primary_cell_v13['modification']]
    value = upgrader.upgrade('primary_cell', primary_cell_v13, current_version='13', target_version='14')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert 'biosample_term' not in value
    assert sample_terms == value['sample_terms']
    assert type(value['sample_terms']) == list
    assert 'modification' not in value
    assert modifications == value['modifications']
    assert type(value['modifications']) == list
    assert value['schema_version'] == '14'


def test_primary_cell_14_15(upgrader, primary_cell_v14_no_units, primary_cell_v14_no_amount):
    value = upgrader.upgrade('primary_cell', primary_cell_v14_no_units, current_version='14', target_version='15')
    assert 'starting_amount_units' in value and value['starting_amount_units'] == 'items'
    assert value['schema_version'] == '15'
    value = upgrader.upgrade('primary_cell', primary_cell_v14_no_amount, current_version='14', target_version='15')
    assert 'starting_amount' in value and value['starting_amount'] == 0
    assert value['schema_version'] == '15'


def test_primary_cell_upgrade_15_16(upgrader, primary_cell_v15):
    sorted_sample = primary_cell_v15['sorted_fraction']
    sorted_sample_detail = primary_cell_v15['sorted_fraction_detail']
    value = upgrader.upgrade('primary_cell', primary_cell_v15, current_version='15', target_version='16')
    assert 'sorted_from' in value and value['sorted_from'] == sorted_sample
    assert 'sorted_from_detail' in value and value['sorted_from_detail'] == sorted_sample_detail
    assert value['schema_version'] == '16'


def test_primary_cell_upgrade_16_17(upgrader, primary_cell_v16):
    value = upgrader.upgrade('primary_cell', primary_cell_v16, current_version='16', target_version='17')
    assert value['schema_version'] == '17'
    assert 'description' not in value
