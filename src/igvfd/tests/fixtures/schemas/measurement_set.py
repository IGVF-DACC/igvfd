import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['STARR-seq']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome(testapp, lab, award, assay_term_atac, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'multiome_size': 2,
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['10x multiome']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome_2(testapp, lab, award, assay_term_rna, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_rna['@id'],
        'multiome_size': 2,
        'samples': [in_vitro_cell_line['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['10x multiome']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_no_files(testapp, lab, award, assay_term_ntr, in_vitro_differentiated_cell):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_ntr['@id'],
        'samples': [in_vitro_differentiated_cell['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['CRISPR FlowFISH screen']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_mpra(testapp, lab, award, assay_term_mpra, primary_cell):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_mpra['@id'],
        'samples': [primary_cell['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['MPRA']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_one_onlist(testapp, lab, award, assay_term_scrna, tissue, tabular_file_onlist_1):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_scrna['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['scRNA-seq'],
        'onlist_files': [tabular_file_onlist_1['@id']],
        'onlist_method': 'no combination'
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_two_onlists(testapp, lab, award, assay_term_scrna, tissue, tabular_file_onlist_1, tabular_file_onlist_2):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_scrna['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['scRNA-seq'],
        'onlist_files': [tabular_file_onlist_1['@id'], tabular_file_onlist_2['@id']],
        'onlist_method': 'product'
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_one_onlist_atac(testapp, lab, award, assay_term_scatac, tissue, tabular_file_onlist_1):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_scatac['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['snATAC-seq'],
        'onlist_files': [tabular_file_onlist_1['@id']],
        'onlist_method': 'no combination'
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_two_onlists_atac(testapp, lab, award, assay_term_scatac, tissue, tabular_file_onlist_1, tabular_file_onlist_2):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_scatac['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['snATAC-seq'],
        'onlist_files': [tabular_file_onlist_1['@id'], tabular_file_onlist_2['@id']],
        'onlist_method': 'product'
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_perturb_seq(testapp, lab, award, assay_term_crispr_single_cell, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_crispr_single_cell['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['Perturb-seq']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_with_protocols(testapp, lab, award, assay_term_starr, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'protocols': ['https://www.protocols.io/test-protocols-url-12345'],
        'preferred_assay_titles': ['STARR-seq']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_with_functional_assay_mechanisms(testapp, lab, award, assay_term_starr, tissue, phenotype_term_from_go):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'preferred_assay_titles': ['STARR-seq'],
        'functional_assay_mechanisms': [phenotype_term_from_go['@id']]
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_v1(measurement_set, in_vitro_cell_line, human_donor):
    item = measurement_set.copy()
    item.update({
        'schema_version': '1',
        'sample': [in_vitro_cell_line['@id']],
        'donor': [human_donor['@id']]
    })
    return item


@pytest.fixture
def measurement_set_v3(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '3',
        'protocols': ['https://www.protocols.io/']
    })
    return item


@pytest.fixture
def measurement_set_v4(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '4',
        'seqspec': 'https://github.com/IGVF/seqspec/blob/main/assays/SHARE-seq/spec.yaml'
    })
    return item


@pytest.fixture
def measurement_set_v5(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '5'
    })
    return item


@pytest.fixture
def measurement_set_v6(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '6',
        'moi': '5',
        'nucleic_acid_delivery': 'adenoviral transduction'
    })
    return item


@pytest.fixture
def measurement_set_v7_multiome(testapp, lab, award, assay_term_atac, tissue):
    item = {
        'schema_version': '7',
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'multiome_size': 2.789,
        'samples': [tissue['@id']]
    }
    return item


@pytest.fixture
def measurement_set_v8(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '8',
        'sequencing_library_type': ['direct RNA', 'exome capture']
    })
    return item


@pytest.fixture
def measurement_set_v9(measurement_set_v8):
    item = measurement_set_v8.copy()
    item.update({
        'schema_version': '9',
        'description': ''
    })
    return item


@pytest.fixture
def measurement_set_v10(testapp, lab, award, assay_term_atac, tissue):
    item = {
        'schema_version': '10',
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'samples': [tissue['@id']]
    }
    return item


@pytest.fixture
def measurement_set_v11(testapp, lab, award, assay_term_atac, tissue):
    item = {
        'schema_version': '11',
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'samples': [tissue['@id']],
        'protocol': 'https://www.protocols.io/test-protocols-url-12345'
    }
    return item


@pytest.fixture
def measurement_set_v12(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '12',
        'preferred_assay_title': 'Parse Split-seq'
    })
    return item


@pytest.fixture
def measurement_set_v14(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '14',
        'protocols': [],
        'control_file_sets': [],
        'sequencing_library_types': [],
        'auxiliary_sets': []
    })
    return item


@pytest.fixture
def measurement_set_v15(measurement_set, tissue, primary_cell):
    item = measurement_set.copy()
    item.update({
        'schema_version': '15',
        'samples': [tissue['@id'], primary_cell['@id']]
    })
    return item


@pytest.fixture
def measurement_set_v16(measurement_set, assay_term_rna):
    item = measurement_set.copy()
    item.update({
        'schema_version': '16',
        'readout': assay_term_rna['@id']
    })
    return item


@pytest.fixture
def measurement_set_v17(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '17',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def measurement_set_v18(measurement_set_v17, platform_term_v3):
    item = measurement_set_v17.copy()
    item.update({
        'schema_version': '18',
        'library_construction_platform': platform_term_v3['@id']
    })
    return item


@pytest.fixture
def measurement_set_v19(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '19',
        'preferred_assay_title': 'CRISPR FlowFISH'
    })
    return item


@pytest.fixture
def measurement_set_v20(lab, award, assay_term_starr, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data',
        'schema_version': '20'
    }
    return item


@pytest.fixture
def measurement_set_v21(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '21',
        'preferred_assay_title': 'Variant painting'
    })
    return item


@pytest.fixture
def measurement_set_v22(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '21',
        'preferred_assay_title': 'Variant FlowFISH'
    })
    return item


@pytest.fixture
def measurement_set_v23(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '23',
        'preferred_assay_title': 'scMito-seq'
    })
    return item


@pytest.fixture
def measurement_set_v24(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '24',
        'preferred_assay_title': 'Growth CRISPR screen'
    })
    return item


@pytest.fixture
def measurement_set_v25_5_prime_to_3_prime(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '25',
        'strand_specificity': '5\' to 3\''
    })
    return item


@pytest.fixture
def measurement_set_v25_3_prime_to_5_prime(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '25',
        'strand_specificity': '3\' to 5\''
    })
    return item


@pytest.fixture
def measurement_set_v26(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '26',
        'control_type': 'control transduction'
    })
    return item


@pytest.fixture
def measurement_set_v27(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '27',
        'preferred_assay_title': 'SUPERSTARR'
    })
    return item


@pytest.fixture
def measurement_set_v28(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '28',
        'preferred_assay_title': '10x multiome with scMito-seq'
    })
    return item


@pytest.fixture
def measurement_set_v29(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '29',
        'preferred_assay_title': 'CERES-seq'
    })
    return item


@pytest.fixture
def measurement_set_v30(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '30',
        'preferred_assay_title': 'semi-qY2H'
    })
    return item


@pytest.fixture
def measurement_set_v31(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '31',
        'control_type': 'pre-selection'
    })
    return item


@pytest.fixture
def measurement_set_v32(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '32',
        'control_type': 'pre-selection'
    })
    return item


@pytest.fixture
def measurement_set_v33(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '33',
        'preferred_assay_title': '10X ATAC with Scale pre-indexing',
    })
    return item


@pytest.fixture
def measurement_set_v35(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '35',
        'preferred_assay_title': 'semi-qY2H'
    })
    return item


@pytest.fixture
def measurement_set_v36(measurement_set):
    item = measurement_set.copy()
    item.update({
        'schema_version': '36',
        'preferred_assay_titles': ['Parse Perturb-seq']
    })
    return item
