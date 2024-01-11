import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']],
        'file_set_type': 'experimental data'
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
        'file_set_type': 'experimental data'
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
        'file_set_type': 'experimental data'
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
        'protocol': 'https://www.protocols.io/'
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
def measurement_set_mpra(testapp, lab, award, assay_term_mpra, primary_cell):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_mpra['@id'],
        'samples': [primary_cell['@id']],
        'file_set_type': 'experimental data'
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


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
