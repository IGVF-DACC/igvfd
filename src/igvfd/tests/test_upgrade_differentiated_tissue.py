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


<<<<<<< HEAD
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
=======
def test_differentiated_tissue_upgrade_5_6(upgrader, differentiated_tissue_v5):
    value = upgrader.upgrade('differentiated_tissue', differentiated_tissue_v5, current_version='5', target_version='6')
>>>>>>> add tests, inserts, upgrades
    assert value['schema_version'] == '6'
