import pytest


@pytest.fixture
def whole_organism(testapp, lab, source, award, rodent_donor, sample_term_whole_organism):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_whole_organism['@id']
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]


@pytest.fixture
def whole_organism_v1(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def whole_organism_part_of(whole_organism):
    item = whole_organism.copy()
    return item


@pytest.fixture
def whole_organism_v2(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '2',
        'aliases': [],
        'donors': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': []
    })
    return item


@pytest.fixture
def whole_organism_v3(whole_organism, phenotype_term_alzheimers):
    item = whole_organism.copy()
    item.update({
        'schema_version': '3',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def whole_organism_v4(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '4',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'embryonic'
    })
    return item


@pytest.fixture
def whole_organism_v4_unknown(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '4',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def whole_organism_v4_90_or_above(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '4',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
    })
    return item


@pytest.fixture
def whole_organism_v5(testapp, lab, source, award, rodent_donor, sample_term_whole_organism):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donor': [rodent_donor['@id']],
        'biosample_term': sample_term_whole_organism['@id']
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]
