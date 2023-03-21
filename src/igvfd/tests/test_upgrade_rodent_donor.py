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
