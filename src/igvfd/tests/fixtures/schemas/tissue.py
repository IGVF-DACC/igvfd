import pytest


@pytest.fixture
def tissue(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'accession': 'IGVFSM1111AAAA',
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [rodent_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']]
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
        'accession': 'IGVFSM0000AAAA',
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']]
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def tissue_v6(testapp, lab, source, award, rodent_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'taxa': 'Mus musculus',
        'donor': [rodent_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']]
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
        'sources': [source['@id']],
        'donors': [rodent_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']],
        'embryonic': True
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def biosample_sorted_child(
        testapp, lab, award, source, tissue_unsorted_parent, human_donor, sample_term_adrenal_gland):
    item = {
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']],
        'sources': [source['@id']],
        'sorted_from': tissue_unsorted_parent['@id'],
        'sorted_from_detail': 'FACS bin 0-10% expression of FEN',
        'award': award['@id'],
        'lab': lab['@id'],
        'nih_institutional_certification': 'NIC000ABCD'
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def tissue_v11(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '11',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def tissue_v12(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '12',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def tissue_v13(lab, award, source, human_donor, sample_term_adrenal_gland, modification):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id'],
        'modification': modification['@id']
    }
    return item


@pytest.fixture
def tissue_v14_no_units(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '14',
        'pmi': 3,
        'starting_amount': 5
    })
    return item


@pytest.fixture
def tissue_v14_no_amount(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '14',
        'pmi_units': 'minute',
        'starting_amount_units': 'g'
    })
    return item


@pytest.fixture
def tissue_v15(tissue, in_vitro_differentiated_cell):
    item = tissue.copy()
    item.update({
        'schema_version': '15',
        'sorted_fraction': in_vitro_differentiated_cell['@id'],
        'sorted_fraction_detail': 'This is a detail about the sorting.'
    })
    return item


@pytest.fixture
def tissue_v16(tissue_v15):
    item = tissue_v15.copy()
    item.update({
        'schema_version': '16',
        'description': ''
    })
    return item
