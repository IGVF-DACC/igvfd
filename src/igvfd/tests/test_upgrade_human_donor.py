import pytest


def test_human_donor_upgrade_1_2(upgrader, human_donor_v1):
    value = upgrader.upgrade('human_donor', human_donor_v1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert 'external_resources' not in value
    assert 'aliases' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'documents' not in value
    assert 'references' not in value
    assert value['schema_version'] == '2'


def test_human_donor_upgrade_2_3(upgrader, human_donor_v2):
    value = upgrader.upgrade('human_donor', human_donor_v2, current_version='2', target_version='3')
    assert 'health_status_history' not in value
    assert value['schema_version'] == '3'


def test_human_donor_upgrade_3_4(upgrader, human_donor_v3):
    ethnicites = human_donor_v3['ethnicity']
    value = upgrader.upgrade('human_donor', human_donor_v3, current_version='3', target_version='4')
    assert 'ethnicity' not in value
    assert ethnicites == value['ethnicities']


def test_human_donor_upgrade_4_5(upgrader, human_donor_v4):
    value = upgrader.upgrade('human_donor', human_donor_v4, current_version='4', target_version='5')
    assert value['accession'] == 'IGVFDO0999HHSA'
    assert value['schema_version'] == '5'


def test_human_donor_upgrade_5_6(upgrader, human_donor_v5):
    value = upgrader.upgrade('human_donor', human_donor_v5, current_version='5', target_version='6')
    assert 'external_resources' not in value
    assert value['schema_version'] == '6'


def test_human_donor_upgrade_6_7(
        upgrader,
        human_donor_v6_single_trait_no_notes,
        human_donor_v6_multiple_traits_no_notes,
        human_donor_v6_single_trait_with_notes):
    value = upgrader.upgrade('human_donor', human_donor_v6_single_trait_no_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'traits: /phenotype-terms/HP_0000648/'
    value = upgrader.upgrade('human_donor', human_donor_v6_multiple_traits_no_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'traits: /phenotype-terms/DOID_10652/  traits: /phenotype-terms/HP_0001658/'
    value = upgrader.upgrade('human_donor', human_donor_v6_single_trait_with_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'This is a note.  traits: /phenotype-terms/DOID_10652/'
