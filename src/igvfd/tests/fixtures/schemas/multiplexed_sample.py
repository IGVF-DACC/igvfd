import pytest


@pytest.fixture
def multiplexed_sample(
        testapp, other_lab, award, tissue, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            tissue['@id'], in_vitro_cell_line['@id']
        ],
        'multiplexing_methods': ['barcode based']
    }
    return testapp.post_json('/multiplexed_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def multiplexed_sample_x2(
        testapp, other_lab, award, multiplexed_sample, primary_cell):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            multiplexed_sample['@id'], primary_cell['@id']
        ],
        'multiplexing_methods': ['barcode based']
    }
    return testapp.post_json('/multiplexed_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def multiplexed_sample_x3(
        testapp, other_lab, award, multiplexed_sample_x2, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            multiplexed_sample_x2['@id'], in_vitro_cell_line['@id']
        ],
        'multiplexing_methods': ['barcode based']
    }
    return testapp.post_json('/multiplexed_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def multiplexed_sample_v1(multiplexed_sample, source):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '1',
        'source': source['@id'],
        'product_id': 'ab272168',
        'lot_id': '0000001'
    })
    return item


@pytest.fixture
def multiplexed_sample_v2(multiplexed_sample, source):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def multiplexed_sample_v3_no_units(multiplexed_sample):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '3',
        'starting_amount': 5
    })
    return item


@pytest.fixture
def multiplexed_sample_v3_no_amount(multiplexed_sample):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '3',
        'starting_amount_units': 'g'
    })
    return item


@pytest.fixture
def multiplexed_sample_v4(multiplexed_sample, in_vitro_differentiated_cell):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '4',
        'sorted_fraction': in_vitro_differentiated_cell['@id'],
        'sorted_fraction_detail': 'This is a detail about the sorting.'
    })
    return item


@pytest.fixture
def multiplexed_sample_v5(multiplexed_sample_v4):
    item = multiplexed_sample_v4.copy()
    item.update({
        'schema_version': '5',
        'description': ''
    })
    return item


@pytest.fixture
def multiplexed_sample_v7(multiplexed_sample):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '7',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def multiplexed_sample_v8(multiplexed_sample, tabular_file_v10):
    item = multiplexed_sample.copy()
    item.update({
        'schema_version': '8',
        'barcode_sample_map': tabular_file_v10['@id']
    })
    return item


@pytest.fixture
def multiplexed_sample_v9(
        testapp, other_lab, award, tissue, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            tissue['@id'], in_vitro_cell_line['@id']
        ]
    }
    return item


@pytest.fixture
def multiplexed_sample_mixed_species(
        testapp, other_lab, award, in_vitro_differentiated_cell, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            in_vitro_differentiated_cell['@id'], in_vitro_cell_line['@id']
        ]
    }
    return item
