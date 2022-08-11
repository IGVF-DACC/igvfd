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
