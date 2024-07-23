import pytest


def test_rodent_donor_upgrade_1_2(upgrader, rodent_donor_v1):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v1, current_version='1', target_version='2')
    assert 'documents' not in value
    assert 'external_resources' not in value
    assert 'aliases' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'references' not in value
    assert value['schema_version'] == '2'


def test_rodent_donor_upgrade_2_3(upgrader, rodent_donor_v2):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v2, current_version='2', target_version='3')
    assert value['accession'] == 'IGVFDO0555MMMA'
    assert value['individual_rodent'] == False
    assert value['schema_version'] == '3'


def test_rodent_donor_upgrade_3_4(upgrader, rodent_donor_v3):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v3, current_version='3', target_version='4')
    assert 'external_resources' not in value
    assert value['individual_rodent'] == False
    assert value['schema_version'] == '4'


def test_rodent_donor_upgrade_4_5(upgrader, rodent_donor_v4):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v4, current_version='4', target_version='5')
    assert value['individual_rodent'] == False
    assert value['schema_version'] == '5'


def test_rodent_donor_upgrade_6_7(upgrader, rodent_donor_v6_with_parents, parent_rodent_donor_1):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v6_with_parents,
                             current_version='6', target_version='7')
    assert 'parents' not in value
    assert value['notes'] == 'This is a note.  parents: ' + parent_rodent_donor_1['@id']


def test_rodent_donor_upgrade_7_8(upgrader, rodent_donor_v7):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['virtual'] == False


def test_rodent_donor_upgrade_9_10(upgrader, rodent_donor_v9):
    sources = [rodent_donor_v9['source']]
    value = upgrader.upgrade('rodent_donor', rodent_donor_v9, current_version='9', target_version='10')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert value['schema_version'] == '10'


def test_rodent_donor_upgrade_10_11(upgrader, rodent_donor_v10):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v10, current_version='10', target_version='11')
    assert 'description' not in value
    assert value['schema_version'] == '11'


def test_rodent_donor_upgrade_12_13(upgrader, rodent_donor_v12):
    value = upgrader.upgrade('rodent_donor', rodent_donor_v12, current_version='12', target_version='13')
    assert 'product_id' not in value
    assert 'notes' in value and value['notes'].endswith('Product_id 100A was removed from this donor.')
    assert value['schema_version'] == '13'
