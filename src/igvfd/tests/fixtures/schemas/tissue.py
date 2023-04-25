import pytest


@pytest.fixture
def tissue(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
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


@pytest.fixture
def tissue_v8(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '8',
        'accession': 'IGVFSM333TTS'
    })
    return item


@pytest.fixture
def tissue_v9(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '9',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def tissue_v10(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '10',
        'taxa': 'Saccharomyces',
        'notes': ''
    })
    return item


@pytest.fixture
def tissue_unsorted_parent(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id'],
        'embryonic': True
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def biosample_sorted_child(
        testapp, lab, award, source, tissue_unsorted_parent, human_donor, sample_term_adrenal_gland):
    item = {
        'donors': [human_donor['@id']],
        'taxa': 'Homo sapiens',
        'biosample_term': sample_term_adrenal_gland['@id'],
        'source': source['@id'],
        'sorted_fraction': tissue_unsorted_parent['@id'],
        'sorted_fraction_detail': 'FACS bin 0-10% expression of FEN',
        'award': award['@id'],
        'lab': lab['@id'],
        'nih_institutional_certification': 'NIC000ABCD'
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]
