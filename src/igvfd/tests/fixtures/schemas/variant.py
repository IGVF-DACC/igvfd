import pytest


@pytest.fixture
def variant(testapp):
    item = {
        'location': [{
            'ref': 'ACTG',
            'alt': 'GTCA'
        }]
    }
    return testapp.post_json('/variant', item, status=201).json['@graph'][0]
