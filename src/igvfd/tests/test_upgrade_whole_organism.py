import pytest


def test_whole_organism_upgrade_1_2(upgrader, whole_organism_v1):
    value = upgrader.upgrade('whole_organism', whole_organism_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_whole_organism_upgrade_2_3(upgrader, whole_organism_v2):
    value = upgrader.upgrade('whole_organism', whole_organism_v2, current_version='2', target_version='3')
    assert 'aliases' not in value
    assert 'donors' not in value
    assert 'dbxrefs' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'treatments' not in value
    assert value['schema_version'] == '3'


def test_whole_organism_upgrade_3_4(upgrader, whole_organism_v3, phenotype_term_alzheimers):
    value = upgrader.upgrade('whole_organism', whole_organism_v3, current_version='3', target_version='4')
    assert 'disease_term' not in value
    assert value['schema_version'] == '4'
    assert value.get('disease_terms') == [phenotype_term_alzheimers['@id']]


def test_whole_organism_upgrade_4_5(upgrader, whole_organism_v4, whole_organism_v4_unknown, whole_organism_v4_90_or_above):
    value = upgrader.upgrade('whole_organism', whole_organism_v4, current_version='4', target_version='5')
    assert value['lower_bound_age'] == 10 and value['upper_bound_age'] == 10
    assert value['embryonic']
    assert 'life_stage' not in value
    assert value['schema_version'] == '5'
    value = upgrader.upgrade('whole_organism', whole_organism_v4_unknown, current_version='4', target_version='5')
    assert 'life_stage' not in value
    assert 'age' not in value
    assert value['schema_version'] == '5'
    value = upgrader.upgrade('whole_organism', whole_organism_v4_90_or_above, current_version='4', target_version='5')
    assert 'life_stage' not in value
    assert value['lower_bound_age'] == 90 and value['upper_bound_age'] == 90
    assert value['schema_version'] == '5'


def test_whole_organism_upgrade_5_6(upgrader, whole_organism_v5):
    assert 'donor' in whole_organism_v5
    value = upgrader.upgrade('whole_organism', whole_organism_v5, current_version='5', target_version='6')
    assert 'donor' not in value
    assert 'donors' in value
    assert value['schema_version'] == '6'


def test_whole_organism_upgrade_6_7(upgrader, whole_organism_v6):
    biomarkers = whole_organism_v6['biomarker']
    value = upgrader.upgrade('whole_organism', whole_organism_v6, current_version='6', target_version='7')
    assert 'biomarker' not in value
    assert biomarkers == value['biomarkers']
    assert value['schema_version'] == '7'


def test_whole_organism_upgrade_7_8(upgrader, whole_organism_v7):
    value = upgrader.upgrade('whole_organism', whole_organism_v7, current_version='7', target_version='8')
    assert value['accession'] == 'IGVFSM0111WWOA'
    assert value['schema_version'] == '8'


def test_whole_organism_upgrade_8_9(upgrader, whole_organism_v8):
    value = upgrader.upgrade('whole_organism', whole_organism_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert value['sorted_fraction_detail'] == 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


def test_whole_organism_upgrade_9_10(upgrader, whole_organism_v9):
    value = upgrader.upgrade('whole_organism', whole_organism_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert value['taxa'] != 'Saccharomyces'
    assert value['notes'] == 'Previous taxa: Saccharomyces is no longer valid.'


def test_whole_organism_upgrade_10_11(upgrader, whole_organism_v10):
    value = upgrader.upgrade('whole_organism', whole_organism_v10, current_version='10', target_version='11')
    assert value['schema_version'] == '11'
    assert 'part_of' not in value
    assert 'pooled_from' not in value


def test_whole_organism_upgrade_11_12(upgrader, whole_organism_v11):
    value = upgrader.upgrade('whole_organism', whole_organism_v11, current_version='11', target_version='12')
    assert value['schema_version'] == '12'
    assert value['biosample_term'] == '/sample-term/UBERON_0000468/'
    assert value['notes'] == 'Biosample_term (formerly: /sample-terms/EFO_0002067/) was automatically upgraded.'
