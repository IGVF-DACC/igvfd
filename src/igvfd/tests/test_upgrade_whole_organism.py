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


def test_whole_organism_upgrade_4_5(
        upgrader,
        whole_organism_v4,
        whole_organism_v4_unknown,
        whole_organism_v4_90_or_above):
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
    assert value['sample_terms'] == ['/sample-terms/UBERON_0000468/']
    assert value['notes'] == 'Biosample_term (formerly: /sample-terms/EFO_0002067/) was automatically upgraded.'


def test_whole_organism_upgrade_12_13(upgrader, whole_organism_v12):
    value = upgrader.upgrade('whole_organism', whole_organism_v12, current_version='12', target_version='13')
    assert value['schema_version'] == '13'
    assert 'taxa' not in value
    assert value['notes'] == 'Previous taxa: Homo sapiens will now be calculated.'


def test_whole_organism_upgrade_13_14(upgrader, whole_organism_v13):
    value = upgrader.upgrade('whole_organism', whole_organism_v13, current_version='13', target_version='14')
    assert value['schema_version'] == '14'
    assert value['virtual'] == False


def test_whole_organism_upgrade_14_15(upgrader, whole_organism_v14):
    value = upgrader.upgrade('whole_organism', whole_organism_v14, current_version='14', target_version='15')
    assert value['schema_version'] == '15'
    assert 'part_of' not in value
    assert 'pooled_from' not in value


def test_whole_organism_upgrade_15_16(upgrader, whole_organism_v15):
    ids = whole_organism_v15['references']
    value = upgrader.upgrade(
        'whole_organism', whole_organism_v15,
        current_version='15', target_version='16')
    assert value['schema_version'] == '16'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_whole_organism_upgrade_16_17(upgrader, whole_organism_v16):
    sources = [whole_organism_v16['source']]
    sample_terms = [whole_organism_v16['biosample_term']]
    modifications = [whole_organism_v16['modification']]
    value = upgrader.upgrade('whole_organism', whole_organism_v16, current_version='16', target_version='17')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert 'biosample_term' not in value
    assert sample_terms == value['sample_terms']
    assert type(value['sample_terms']) == list
    assert 'modification' not in value
    assert modifications == value['modifications']
    assert type(value['modifications']) == list
    assert value['schema_version'] == '17'


def test_whole_organism_upgrade_17_18(upgrader, whole_organism_v17_no_units, whole_organism_v17_no_amount):
    value = upgrader.upgrade('whole_organism', whole_organism_v17_no_units, current_version='17', target_version='18')
    assert 'starting_amount_units' in value and value['starting_amount_units'] == 'items'
    assert value['schema_version'] == '18'
    value = upgrader.upgrade('whole_organism', whole_organism_v17_no_amount, current_version='17', target_version='18')
    assert 'starting_amount' in value and value['starting_amount'] == 0
    assert value['schema_version'] == '18'


def test_whole_organism_upgrade_18_19(upgrader, whole_organism_v18):
    sorted_sample = whole_organism_v18['sorted_fraction']
    sorted_sample_detail = whole_organism_v18['sorted_fraction_detail']
    value = upgrader.upgrade('whole_organism', whole_organism_v18, current_version='18', target_version='19')
    assert 'sorted_from' in value and value['sorted_from'] == sorted_sample
    assert 'sorted_from_detail' in value and value['sorted_from_detail'] == sorted_sample_detail
    assert value['schema_version'] == '19'


def test_whole_organism_upgrade_19_20(upgrader, whole_organism_v19):
    value = upgrader.upgrade('whole_organism', whole_organism_v19, current_version='19', target_version='20')
    assert value['schema_version'] == '20'
    assert 'description' not in value


def test_whole_organism_upgrade_21_22(upgrader, whole_organism_v21):
    value = upgrader.upgrade('whole_organism', whole_organism_v21, current_version='21', target_version='22')
    assert value['schema_version'] == '22'
    assert 'nih_institutional_certification' not in value


def test_whole_organism_upgrade_22_23(upgrader, whole_organism_v22):
    value = upgrader.upgrade('whole_organism', whole_organism_v22, current_version='22', target_version='23')
    assert value['schema_version'] == '23'
    assert 'product_id' not in value
    assert 'notes' in value and value['notes'].endswith(
        'Product_id 100A was removed from this sample. Lot_id 123 was removed from this sample.')


def test_whole_organism_upgrade_23_24(upgrader, whole_organism_v23):
    value = upgrader.upgrade('whole_organism', whole_organism_v23, current_version='23', target_version='24')
    assert 'publication_identifiers' not in value
    assert value['schema_version'] == '24'
