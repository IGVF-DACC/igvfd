import pytest


@pytest.fixture
def in_vitro_cell_line(testapp, other_lab, award, rodent_donor, sample_term_K562):
    item = {
        'classification': 'cell line',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
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
        'donors': [human_donor['@id']],
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
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_system_v1(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'classification': 'differentiated tissue',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donor': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return item


@pytest.fixture
def in_vitro_system_v2(in_vitro_cell_line, biomarker_CD1e_low):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '2',
        'biomarker': [biomarker_CD1e_low['@id']]
    })
    return item
