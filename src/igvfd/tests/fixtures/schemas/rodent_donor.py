import pytest


@pytest.fixture
def rodent_donor(testapp, lab, taxon_id, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': taxon_id['@id']
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]
