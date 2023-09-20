import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id'],
        'samples': [tissue['@id']]
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome(testapp, lab, award, assay_term_atac, tissue):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'multiome_size': 2,
        'samples': [tissue['@id']]
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome_2(testapp, lab, award, assay_term_rna, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_rna['@id'],
        'multiome_size': 2,
        'samples': [in_vitro_cell_line['@id']]
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
        'samples': primary_cell['@id']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]
