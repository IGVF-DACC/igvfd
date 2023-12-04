import pytest


def test_human_donor_upgrade_1_2(upgrader, human_donor_v1):
    value = upgrader.upgrade('human_donor', human_donor_v1, current_version='1', target_version='2')
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


def test_human_donor_upgrade_6_7(upgrader, human_donor_v6_single_trait_no_notes, human_donor_v6_multiple_traits_no_notes, human_donor_v6_single_trait_with_notes, phenotype_term_alzheimers, phenotype_term_myocardial_infarction):
    value = upgrader.upgrade('human_donor', human_donor_v6_single_trait_no_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'traits: ' + phenotype_term_alzheimers['@id']
    value = upgrader.upgrade('human_donor', human_donor_v6_multiple_traits_no_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'traits: ' + phenotype_term_alzheimers['@id'] + \
        '  traits: ' + phenotype_term_myocardial_infarction['@id']
    value = upgrader.upgrade('human_donor', human_donor_v6_single_trait_with_notes,
                             current_version='6', target_version='7')
    assert 'traits' not in value
    assert value['notes'] == 'This is a note.  traits: ' + phenotype_term_alzheimers['@id']


def test_human_donor_upgrade_7_8(upgrader, human_donor_v7_with_parents, parent_human_donor_1, parent_human_donor_2):
    value = upgrader.upgrade('human_donor', human_donor_v7_with_parents,
                             current_version='7', target_version='8')
    assert 'parents' not in value
    assert {
        'donor': parent_human_donor_1['@id'],
        'relationship_type': 'parent'
    } in value['related_donors']
    assert {
        'donor': parent_human_donor_2['@id'],
        'relationship_type': 'parent'
    } in value['related_donors']


def test_human_donor_upgrade_8_9(upgrader, human_donor_v8):
    value = upgrader.upgrade('human_donor', human_donor_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert value['virtual'] == False


def test_human_donor_upgrade_9_10(upgrader, human_donor_v9):
    identifiers = human_donor_v9['human_donor_identifier']
    value = upgrader.upgrade('human_donor', human_donor_v9, current_version='9', target_version='10')
    assert 'human_donor_identifier' not in value
    assert identifiers == value['human_donor_identifiers']


def test_human_donor_upgrade_11_12(upgrader, human_donor_v11):
    value = upgrader.upgrade('human_donor', human_donor_v11, current_version='11', target_version='12')
    assert 'description' not in value
    assert value['schema_version'] == '12'
