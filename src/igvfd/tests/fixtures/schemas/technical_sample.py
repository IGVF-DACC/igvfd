import pytest


@pytest.fixture
def technical_sample_1(testapp, other_lab, award):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id']
    }
    return testapp.post_json('/technical_sample', item, status=201).json['@graph'][0]
