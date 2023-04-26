import pytest


@pytest.fixture
def in_vitro_cell_line(testapp, other_lab, award, rodent_donor, sample_term_K562):
    item = {
        'classification': 'cell line',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_differentiated_cell(testapp, lab, award, source, human_donor, sample_term_K562):
    item = {
        'classification': 'differentiated cell specimen',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_organoid(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'classification': 'organoid',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_system_v1(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'classification': 'organoid',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
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


@pytest.fixture
def in_vitro_system_v3(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '3',
        'accession': 'IGVFSM222IIV'
    })
    return item


@pytest.fixture
def in_vitro_system_v4(in_vitro_organoid):
    item = in_vitro_organoid.copy()
    item.update({
        'schema_version': '4',
        'classification': 'differentiated tissue'
    })
    return item


@pytest.fixture
def in_vitro_system_v5(in_vitro_organoid):
    item = in_vitro_organoid.copy()
    item.update({
        'schema_version': '5',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def in_vitro_system_v6(in_vitro_system_v1):
    item = in_vitro_system_v1.copy()
    item.update({
        'schema_version': '6',
        'taxa': 'Saccharomyces',
        'notes': ''
    })
    return item


@pytest.fixture
def in_vitro_system_v7(in_vitro_organoid):
    item = in_vitro_organoid.copy()
    item.update({
        'schema_version': '7',
        'classification': 'differentiated cell'
    })
    return item
