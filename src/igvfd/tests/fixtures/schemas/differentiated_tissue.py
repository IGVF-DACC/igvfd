import pytest


@pytest.fixture
def differentiated_tissue(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donor': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/differentiated_tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def differentiated_tissue_v1(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def differentiated_tissue_part_of(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'alias': 'igvf-dacc:differentiated_tissue_part_of'
    })
    return item


@pytest.fixture
def differentiated_tissue_v2(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def differentiated_tissue_v3(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '3',
        'aliases': [],
        'donor': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': [],
        'differentiation_treatments': []
    })
    return item


@pytest.fixture
def differentiated_tissue_v4(differentiated_tissue, phenotype_term_alzheimers):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def differentiated_tissue_v5(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'embryonic'
    })
    return item


@pytest.fixture
def differentiated_tissue_v5_unknown(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def differentiated_tissue_v5_90_or_above(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
    })
    return item


@pytest.fixture
def differentiated_tissue_v6(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '6',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage'
    })
    return item


@pytest.fixture
def differentiated_tissue_v6_good_value(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '6',
        'post_differentiation_time': 7,
        'post_differentiation_time_units': 'month'
    })
    return item


@pytest.fixture
def differentiated_tissue_v6_with_note(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '6',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage',
        'notes': 'This is a note.'
    })
    return item


@pytest.fixture
def differentiated_tissue_v7(differentiated_tissue, document_v1, differentiated_tissue_v6_good_value, treatment_chemical, phenotype_term_alzheimers):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '7',
        'aliases': ['igvf:differentiated_tissue_v7'],
        'alternate_accessions': ['IGVFSM999QWE'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']],
        'part_of': differentiated_tissue_v6_good_value['@id'],
        'treatments': [treatment_chemical['@id']],
        'differentiated_treatments': [treatment_chemical['@id']],
        'disease_terms': [phenotype_term_alzheimers['@id']],
        'dbxrefs': ['GEO:SAMN1']
    })
    return item
