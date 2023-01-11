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
    assert 'donors' in primary_cell_v6
    value = upgrader.upgrade('primary_cell', primary_cell_v6, current_version='6', target_version='7')
    assert 'donor' not in value
    assert value['schema_version'] == '7'
