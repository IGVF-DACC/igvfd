import pytest


@pytest.fixture
def base_auxiliary_set(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'auxiliary_type': 'gRNA sequencing'
    }
    return testapp.post_json('/auxiliary_set', item).json['@graph'][0]
