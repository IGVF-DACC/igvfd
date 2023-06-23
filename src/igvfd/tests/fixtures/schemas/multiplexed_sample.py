import pytest


@pytest.fixture
def multiplexed_sample(
        testapp, other_lab, award, source, tissue, in_vitro_cell_line):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': source['@id'],
        'multiplexed_samples': [
            tissue['@id'], in_vitro_cell_line['@id']
        ]
    }
    return testapp.post_json('/multiplexed_sample', item, status=201).json['@graph'][0]
