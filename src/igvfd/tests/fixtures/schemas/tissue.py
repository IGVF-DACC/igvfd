import pytest


@pytest.fixture
def tissue(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def tissue_v1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def tissue_part_of(tissue):
    item = tissue.copy()
    item.update({
        'aliases': 'igvf-dacc:tissue_part_of'
    })
    return item


@pytest.fixture
def tissue_v2(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def tissue_v3(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '3',
        'aliases': [],
        'donors': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': []
    })
    return item


@pytest.fixture
def tissue_v4(tissue, phenotype_term_alzheimers):
    item = tissue.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def tissue_v5(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '5',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'embryonic'
    })
    return item


@pytest.fixture
def tissue_v5_unknown(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '5',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def tissue_v5_90_or_above(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '5',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
    })
    return item


@pytest.fixture
def human_tissue(testapp, lab, source, award, human_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def tissue_v6(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donor': [rodent_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return item


@pytest.fixture
def tissue_v7(tissue, biomarker_CD1e_low):
    item = tissue.copy()
    item.update({
        'schema_version': '7',
        'biomarker': [biomarker_CD1e_low['@id']]
    })
    return item
