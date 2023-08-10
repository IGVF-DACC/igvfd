import pytest


@pytest.fixture
def multiplexed_sample(
        testapp, other_lab, award, tissue, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'multiplexed_samples': [
            tissue['@id'], in_vitro_cell_line['@id']
        ]
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
