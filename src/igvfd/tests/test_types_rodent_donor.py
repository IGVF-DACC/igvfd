import pytest


def test_rodent_donor_duplicate_strain_sex(testapp, lab, award):
    item1 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain10',
        'sex': 'female'
    }
    response1 = testapp.post_json('/rodent_donor', item1, status=201)
    assert response1.status_code == 201
    item2 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain10',
        'sex': 'female'
    }
    response2 = testapp.post_json('/rodent_donor', item2, status=409)
    assert response2.status_code == 409


def test_human_donor_summary(testapp, rodent_donor):
    res = testapp.get(rodent_donor['@id'])
    assert res.json.get('summary') == 'strain1 male'
