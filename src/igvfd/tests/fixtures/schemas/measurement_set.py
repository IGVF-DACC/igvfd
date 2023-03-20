import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome(testapp, lab, award, assay_term_atac):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_atac['@id'],
        'multiome_size': 2
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_multiome_2(testapp, lab, award, assay_term_rna):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_rna['@id'],
        'multiome_size': 2
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
