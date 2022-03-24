import pytest


@pytest.fixture
def sample_1(testapp, other_lab, award):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': "j-michael-cherry",
    }
    return testapp.post_json('/sample', item, status=201).json['@graph'][0]
