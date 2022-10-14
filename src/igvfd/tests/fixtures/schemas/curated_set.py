import pytest


@pytest.fixture
def curated_set_genome(testapp, lab, award):
    item = {
        'curated_set_type': 'genome',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/curated_set', item).json['@graph'][0]
