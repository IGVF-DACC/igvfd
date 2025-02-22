import pytest


@pytest.fixture
def primary_cell(testapp, other_lab, award, human_donor, sample_term_pluripotent_stem_cell):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [other_lab['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']]
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def pooled_from_primary_cell(testapp, lab, award, source, human_donor, sample_term_pluripotent_stem_cell):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']],
        'virtual': False,
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def pooled_from_primary_cell_2(testapp, lab, award, source, human_donor, sample_term_pluripotent_stem_cell):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']],
        'virtual': False,
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def primary_cell_with_pooled_from(testapp, other_lab, award, human_donor, sample_term_pluripotent_stem_cell, pooled_from_primary_cell, pooled_from_primary_cell_2):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [other_lab['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']],
        'virtual': True,
        'pooled_from': [pooled_from_primary_cell['@id'], pooled_from_primary_cell_2['@id']]
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def primary_cell_with_part_of_virtual_true(testapp, other_lab, award, human_donor, sample_term_pluripotent_stem_cell, primary_cell):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [other_lab['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']],
        'virtual': False,
        'part_of': primary_cell['@id']
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def primary_cell_v1(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def primary_cell_part_of(primary_cell):
    item = primary_cell.copy()
    item.update({
        'aliases': 'igvf-dacc:primary_cell_part_of'
    })
    return item


@pytest.fixture
def primary_cell_v2(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def primary_cell_v3(primary_cell):
    item = primary_cell.copy()
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
def primary_cell_v4(primary_cell, phenotype_term_alzheimers):
    item = primary_cell.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def primary_cell_v5(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '5',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'embryonic'
    })
    return item


@pytest.fixture
def primary_cell_v5_unknown(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '5',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def primary_cell_v5_90_or_above(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '5',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
    })
    return item


@pytest.fixture
def primary_cell_v6(testapp, other_lab, award, human_donor, sample_term_pluripotent_stem_cell):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [other_lab['@id']],
        'donor': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']]
    }
    return item


@pytest.fixture
def primary_cell_v7(primary_cell, biomarker_CD1e_low):
    item = primary_cell.copy()
    item.update({
        'schema_version': '7',
        'biomarker': [biomarker_CD1e_low['@id']]
    })
    return item


@pytest.fixture
def primary_cell_v8(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '8',
        'accession': 'IGVFSM666PPC'
    })
    return item


@pytest.fixture
def primary_cell_v9(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '9',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def primary_cell_v10(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '10',
        'taxa': 'Saccharomyces',
        'notes': ''
    })
    return item


@pytest.fixture
def primary_cell_v11(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '11',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def primary_cell_v12(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '12',
        'taxa': 'Homo sapiens',
        'notes': ''
    })
    return item


@pytest.fixture
def primary_cell_v13(lab, award, source, human_donor, sample_term_adrenal_gland, crispr_modification):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id'],
        'modification': crispr_modification['@id']
    }
    return item


@pytest.fixture
def primary_cell_v14_no_units(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '14',
        'starting_amount': 5
    })
    return item


@pytest.fixture
def primary_cell_v14_no_amount(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '14',
        'starting_amount_units': 'g'
    })
    return item


@pytest.fixture
def primary_cell_v15(primary_cell, in_vitro_differentiated_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '15',
        'sorted_fraction': in_vitro_differentiated_cell['@id'],
        'sorted_fraction_detail': 'This is a detail about the sorting.'
    })
    return item


@pytest.fixture
def primary_cell_v16(primary_cell_v15):
    item = primary_cell_v15.copy()
    item.update({
        'schema_version': '16',
        'description': ''
    })
    return item


@pytest.fixture
def primary_cell_v17(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '17',
        'status': 'released'
    })
    return item


@pytest.fixture
def primary_cell_v18(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '18',
        'nih_institutional_certification': 'NIC00017'
    })
    return item


@pytest.fixture
def primary_cell_v19(testapp, other_lab, award, human_donor, sample_term_pluripotent_stem_cell):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_pluripotent_stem_cell['@id']],
        'product_id': '100A',
        'lot_id': '123'
    }
    return item


@pytest.fixture
def primary_cell_v20(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '20',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def primary_cell_v21(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '21',
        'biosample_qualifiers': ['calcified']
    })
    return item
