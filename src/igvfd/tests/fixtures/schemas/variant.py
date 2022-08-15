import pytest


@pytest.fixture
def variant(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'locations': [{
            'assembly': 'GRCh38',
            'chromosome': 'chr1',
            'position': 1000000
        }]
    }
    return testapp.post_json('/variant', item, status=201).json['@graph'][0]
