import pytest


@pytest.fixture
def in_vitro_cell_line(testapp, other_lab, award, rodent_donor, sample_term_K562):
    item = {
        'accession': 'IGVFSM2222BBBB',
        'classifications': ['cell line'],
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [other_lab['@id']],
        'donors': [rodent_donor['@id']],
        'sample_terms': [sample_term_K562['@id']]
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_differentiated_cell(testapp, lab, award, source, human_donor, sample_term_K562, treatment_chemical, sample_term_brown_adipose_tissue):
    item = {
        'classifications': ['differentiated cell specimen'],
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_K562['@id']],
        'cell_fate_change_treatments': [treatment_chemical['@id']],
        'time_post_change': 5,
        'time_post_change_units': 'minute',
        'targeted_sample_term': sample_term_brown_adipose_tissue['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_organoid(testapp, lab, award, source, human_donor, sample_term_adrenal_gland, treatment_protein):
    item = {
        'classifications': ['organoid'],
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']],
        'cell_fate_change_treatments': [treatment_protein['@id']],
        'time_post_change': 10,
        'time_post_change_units': 'day',
        'targeted_sample_term': sample_term_adrenal_gland['@id']
    }
    return testapp.post_json('/in_vitro_system', item, status=201).json['@graph'][0]


@pytest.fixture
def in_vitro_system_v1(testapp, lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'classification': 'organoid',
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donor': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']]
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


@pytest.fixture
def in_vitro_system_v8(in_vitro_system_v1):
    item = in_vitro_system_v1.copy()
    item.update({
        'schema_version': '8',
        'taxa': 'Homo sapiens',
        'notes': 'Test.'
    })
    return item


@pytest.fixture
def in_vitro_system_v9(in_vitro_organoid):
    item = in_vitro_organoid.copy()
    item.update({
        'schema_version': '9'
    })
    return item


@pytest.fixture
def in_vitro_system_sub(lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']],
        'classifications': ['embryoid']
    }
    return item


@pytest.fixture
def in_vitro_system_v10(in_vitro_organoid):
    item = in_vitro_organoid.copy()
    item.update({
        'schema_version': '10'
    })
    return item


@pytest.fixture
def in_vitro_system_v11(in_vitro_cell_line, treatment_chemical, sample_term_brown_adipose_tissue):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '11',
        'introduced_factors': [treatment_chemical['@id']],
        'time_post_factors_introduction': 10,
        'time_post_factors_introduction_units': 'minute'
    })
    return item


@pytest.fixture
def in_vitro_system_v12(lab, award, source, human_donor, sample_term_adrenal_gland, crispr_modification):
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
def in_vitro_system_v13_no_units(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '13',
        'starting_amount': 5
    })
    return item


@pytest.fixture
def in_vitro_system_v13_no_amount(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '13',
        'starting_amount_units': 'g'
    })
    return item


@pytest.fixture
def in_vitro_system_v14(in_vitro_cell_line, in_vitro_differentiated_cell):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '14',
        'sorted_fraction': in_vitro_differentiated_cell['@id'],
        'sorted_fraction_detail': 'This is a detail about the sorting.'
    })
    return item


@pytest.fixture
def in_vitro_system_v15(in_vitro_system_v14):
    item = in_vitro_system_v14.copy()
    item.update({
        'schema_version': '15',
        'description': ''
    })
    return item


@pytest.fixture
def in_vitro_system_v16(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '16'
    })
    return item


@pytest.fixture
def in_vitro_system_v17(
    in_vitro_system_v1,
    treatment_protein,
    sample_term_endothelial_cell
):
    item = in_vitro_system_v1.copy()
    item.update({
        'schema_version': '17',
        'classification': 'cell line',
        'time_post_change': 10,
        'time_post_change_units': 'day',
        'cell_fate_change_treatments': [treatment_protein['@id']],
        'targeted_sample_term': sample_term_endothelial_cell['@id']
    })
    return item


@pytest.fixture
def in_vitro_system_v18(lab, award, source, human_donor, sample_term_adrenal_gland):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_adrenal_gland['@id']],
        'classification': 'embryoid'
    }
    return item


@pytest.fixture
def in_vitro_system_v20(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '20',
        'nih_institutional_certification': 'NIC00017'
    })
    return item


@pytest.fixture
<<<<<<< HEAD
def in_vitro_system_v21(testapp, other_lab, award, rodent_donor, sample_term_K562):
    item = {
        'accession': 'IGVFSM2222BBBB',
        'classifications': ['cell line'],
        'award': award['@id'],
        'lab': other_lab['@id'],
        'product_id': '100A',
        'lot_id': '123',
        'donors': [rodent_donor['@id']],
        'sample_terms': [sample_term_K562['@id']]
    }
=======
def in_vitro_system_v22(in_vitro_cell_line):
    item = in_vitro_cell_line.copy()
    item.update({
        'schema_version': '22',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
>>>>>>> 3758549b (upgrade + tests)
    return item
