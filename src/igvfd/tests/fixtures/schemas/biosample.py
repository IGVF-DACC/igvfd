import pytest


@pytest.fixture
def biosample_1(testapp, other_lab, award):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id']
    }
    return testapp.post_json('/biosample', item, status=201).json['@graph'][0]
