import pytest


@pytest.fixture
def human_variant(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'locations': [{
            'assembly': 'GRCh38',
            'position': 1000000
        }]
    }
    return testapp.post_json('/human_variant', item, status=201).json['@graph'][0]
