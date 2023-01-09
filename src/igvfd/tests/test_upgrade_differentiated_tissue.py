import pytest


def test_differentiated_tissue_upgrade_1_2(upgrader, differentiated_tissue_v1):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'


def test_differentiated_tissue_upgrade_2_3(upgrader, differentiated_tissue_v2):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_differentiated_tissue_upgrade_3_4(upgrader, differentiated_tissue_v3):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v3, current_version='3', target_version='4')
    assert 'aliases' not in value
    assert 'donors' not in value
    assert 'dbxrefs' not in value
    assert 'collections' not in value
    assert 'alternate_accessions' not in value
    assert 'treatments' not in value
    assert 'differentiation_treatments' not in value
    assert value['schema_version'] == '4'


def test_differentiated_tissue_upgrade_4_5(upgrader, differentiated_tissue_v4, phenotype_term_alzheimers):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v4, current_version='4', target_version='5')
    assert 'disease_term' not in value
    assert value['schema_version'] == '5'
    assert value.get('disease_terms') == [phenotype_term_alzheimers['@id']]


def test_differentiated_tissue_upgrade_5_6(upgrader, differentiated_tissue_v5, differentiated_tissue_v5_unknown, differentiated_tissue_v5_90_or_above):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v5, current_version='5', target_version='6')
    assert value['lower_bound_age'] == 10 and value['upper_bound_age'] == 10
    assert value['embryonic']
    assert 'life_stage' not in value
    assert value['schema_version'] == '6'
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v5_unknown,
                             current_version='5', target_version='6')
    assert 'life_stage' not in value
    assert 'age' not in value
    assert value['schema_version'] == '6'
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v5_90_or_above,
                             current_version='5', target_version='6')
    assert 'life_stage' not in value
    assert value['lower_bound_age'] == 90 and value['upper_bound_age'] == 90
    assert value['schema_version'] == '6'


def test_differentiated_tissue_upgrade_6_7(upgrader, differentiated_tissue_v6, differentiated_tissue_v6_with_note, differentiated_tissue_v6_good_value):
    value1 = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v6,
                              current_version='6', target_version='7')
    assert value1['schema_version'] == '7'
    assert value1['notes'] == 'post_differentiation_time: 10, post_differentiation_time_units: stage.'
    assert 'post_differentiation_time' not in value1
    assert 'post_differentiation_time_units' not in value1
    value2 = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v6_with_note,
                              current_version='6', target_version='7')
    assert value2['schema_version'] == '7'
    assert value2['notes'] == 'This is a note.  post_differentiation_time: 10, post_differentiation_time_units: stage.'
    assert 'post_differentiation_time' not in value2
    assert 'post_differentiation_time_units' not in value2
    value3 = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v6_good_value,
                              current_version='6', target_version='7')
    assert value3['schema_version'] == '7'
    assert value3['post_differentiation_time'] == 7
    assert value3['post_differentiation_time_units'] == 'month'


def test_differentiated_tissue_upgrade_7_8(upgrader, differentiated_tissue_v7):
    alias = differentiated_tissue_v7['aliases']
    alternate_accession = differentiated_tissue_v7['alternate_accessions']
    collection = differentiated_tissue_v7['collections']
    document = differentiated_tissue_v7['documents']
    treatment = differentiated_tissue_v7['treatments']
    disease_term = differentiated_tissue_v7['disease_terms']
    dbxref = differentiated_tissue_v7['dbxrefs']
    differentiation_treatment = differentiated_tissue_v7['differentiation_treatments']
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v7, current_version='7', target_version='8')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'alternate_accessions' not in value
    assert alternate_accession == value['alternate_accession']
    assert 'collections' not in value
    assert collection == value['collection']
    assert 'documents' not in value
    assert document == value['document']
    assert 'treatments' not in value
    assert treatment == value['treatment']
    assert 'disease_terms' not in value
    assert disease_term == value['disease_term']
    assert 'dbxrefs' not in value
    assert dbxref == value['dbxref']
    assert 'differentiation_treatments' not in value
    assert differentiation_treatment == value['differentiation_treatment']
    assert type(differentiated_tissue_v7['part_of']) is list
    assert value['schema_version'] == '8'
