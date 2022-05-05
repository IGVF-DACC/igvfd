import pytest


def test_rodent_donor_duplicate_strain_sex(testapp, lab, award):
    item1 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'Mus musculus',
        'strain': 'strain10',
        'sex': 'female'
    }
    response1 = testapp.post_json('/rodent_donor', item1, status=201)
    assert(response1.status_code == 201)
    item2 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxon_id': 'Mus musculus',
        'strain': 'strain10',
        'sex': 'female'
    }
    response2 = testapp.post_json('/rodent_donor', item2, status=409)
    assert(response2.status_code == 409)
