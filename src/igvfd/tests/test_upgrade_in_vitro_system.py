import pytest


def test_in_vitro_system_upgrade_7_8(upgrader, in_vitro_system_v1):
    alias = in_vitro_system_v1['aliases']
    alternate_accession = in_vitro_system_v1['alternate_accessions']
    collection = in_vitro_system_v1['collections']
    document = in_vitro_system_v1['documents']
    treatment = in_vitro_system_v1['treatments']
    disease_term = in_vitro_system_v1['disease_terms']
    dbxref = in_vitro_system_v1['dbxrefs']
    disease_term = in_vitro_system_v1['disease_terms']
    introduced_factor = in_vitro_system_v1['introduced_factors']
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v1, current_version='1', target_version='2')
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
    assert 'introduced_factors' not in value
    assert introduced_factor == value['introduced_factor']
    assert type(in_vitro_system_v1['part_of']) is list
    assert type(in_vitro_system_v1['originated_from']) is list
    assert value['schema_version'] == '2'
