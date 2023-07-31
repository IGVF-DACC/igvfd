import pytest


@pytest.fixture
def whole_organism(testapp, lab, source, award, rodent_donor, sample_term_whole_organism):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [rodent_donor['@id']],
        'sample_terms': [sample_term_whole_organism['@id']]
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
        'sources': [source['@id']],
        'taxa': 'Mus musculus',
        'donor': [rodent_donor['@id']],
        'sample_terms': [sample_term_whole_organism['@id']]
    }
    return item


@pytest.fixture
def whole_organism_v6(whole_organism, biomarker_CD1e_low):
    item = whole_organism.copy()
    item.update({
        'schema_version': '6',
        'biomarker': [biomarker_CD1e_low['@id']]
    })
    return item


@pytest.fixture
def whole_organism_v7(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '7',
        'accession': 'IGVFSM111WWO'
    })
    return item


@pytest.fixture
def whole_organism_v8(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '8',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def whole_organism_v9(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '9',
        'taxa': 'Saccharomyces',
        'notes': ''
    })
    return item


@pytest.fixture
def whole_organism_v10(whole_organism, primary_cell, tissue, human_tissue):
    item = whole_organism.copy()
    item.update({
        'schema_version': '10',
        'part_of': primary_cell['@id'],
        'pooled_from': [tissue['@id'], human_tissue['@id']]
    })
    return item


@pytest.fixture
def whole_organism_v11(whole_organism, sample_term_K562):
    item = whole_organism.copy()
    item.update({
        'schema_version': '11',
        'sample_terms': [sample_term_K562['@id']]
    })
    return item


@pytest.fixture
def whole_organism_v12(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '12',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def whole_organism_human(testapp, lab, source, award, human_donor, sample_term_whole_organism):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_whole_organism['@id']]
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]


@pytest.fixture
def whole_organism_v13(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '13',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def whole_organism_v14(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '14',
        'part_of': 'Null',
        'pooled_from': 'Null'
    })
    return item


@pytest.fixture
def whole_organism_v15(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '15',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def whole_organism_v16(lab, award, source, human_donor, sample_term_adrenal_gland, modification):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id'],
        'modification': modification['@id'],
        'schema_version': '16'
    }
    return item
