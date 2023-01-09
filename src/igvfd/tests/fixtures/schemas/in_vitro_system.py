import pytest


@pytest.fixture
def in_vitro_cell_line(testapp, other_lab, award, rodent_donor, sample_term_K562):
    item = {
        'classification': 'cell line',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'taxa': 'Mus musculus',
        'donor': [rodent_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_differentiated_cell(testapp, lab, award, source, human_donor, sample_term_K562):
    item = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donor': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_differentiated_tissue(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'classification': 'differentiated tissue',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donor': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_system_v1(in_vitro_cell_line, document_v1, in_vitro_differentiated_cell, treatment_chemical, phenotype_term_alzheimers, in_vitro_differentiated_tissue):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '1',
        'aliases': ['igvf:in_vitro_system_v1'],
        'alternate_accessions': ['IGVFSM056ATY'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']],
        'part_of': in_vitro_differentiated_cell['@id'],
        'treatments': [treatment_chemical['@id']],
        'disease_terms': [phenotype_term_alzheimers['@id']],
        'dbxrefs': ['GEO:SAMN1'],
        'introduced_factors': [treatment_chemical['@id']],
        'originated_from': [in_vitro_differentiated_tissue['@id']]
    })
    return item
