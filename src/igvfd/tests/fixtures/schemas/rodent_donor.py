import pytest


@pytest.fixture
def rodent_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'NCBI:txid10090',
        'strain': 'strain1',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor1(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'NCBI:txid10090',
        'strain': 'strain2',
        'sex': 'female'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor2(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'NCBI:txid10090',
        'strain': 'strain3',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor3(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'NCBI:txid10090',
        'strain': 'strain4',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def rodent_donor_orphan(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'NCBI:txid10090',
        'strain': 'strain5',
        'sex': 'female'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]
