import pytest


@pytest.fixture
def base_prediction_set(testapp, lab, award, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'functional effect',
        'samples': [in_vitro_cell_line['@id']]
    }
    return testapp.post_json('/prediction_set', item).json['@graph'][0]


@pytest.fixture
def prediction_set_functional_effect(testapp, lab, award, multiplexed_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'functional effect',
        'samples': [multiplexed_sample['@id']]
    }
    return testapp.post_json('/prediction_set', item).json['@graph'][0]


@pytest.fixture
def prediction_set_activity_level(testapp, lab, award, multiplexed_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'activity level',
        'samples': [multiplexed_sample['@id']]
    }
    return testapp.post_json('/prediction_set', item).json['@graph'][0]


@pytest.fixture
def prediction_set_v1(base_prediction_set):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def prediction_set_v2(prediction_set_v1):
    item = prediction_set_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def prediction_set_v3(base_prediction_set, gene_myc_hs):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '3',
        'targeted_loci': {
            'assembly': 'GRCh38',
            'chromosome': 'chr1',
            'start': 1,
            'end': 10
        },
        'targeted_genes': [gene_myc_hs['@id']]
    })
    return item


@pytest.fixture
def prediction_set_v4(base_prediction_set, gene_myc_hs):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '4',
        'genes': [gene_myc_hs['@id']],
    })
    return item


@pytest.fixture
def prediction_set_v5(base_prediction_set):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '5',
        'small_scale_loci_list': [{
            'assembly': 'hg19',
            'chromosome': 'chr1',
            'start': 1,
            'end': 10
        }]
    })
    return item


@pytest.fixture
def prediction_set_v7(base_prediction_set):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '7',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def prediction_set_v8(base_prediction_set):
    item = base_prediction_set.copy()
    item.update({
        'schema_version': '8',
        'file_set_type': 'pathogenicity'
    })
    return item
