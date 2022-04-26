import pytest


def test_differentiation_dependency(in_vitro, testapp):
    res = testapp.patch_json(
        in_vitro['@id'],
        {'post_differentiation_time': 10}, expect_errors=True)
    assert(res.status_code == 422)

    res = testapp.patch_json(
        in_vitro['@id'],
        {'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert(res.status_code == 422)

    res = testapp.patch_json(
        in_vitro['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert(res.status_code == 200)


<<<<<<< HEAD
def test_post_in_vitro(testapp, award, lab, treatment_2):
=======
def test_post_in_vitro(testapp, award, lab):
>>>>>>> 08759e2 (tests)
    res = testapp.post_json(
        '/in_vitro',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'minute',
<<<<<<< HEAD
            'treatments': [treatment_2['@id']]
=======
            'treatment': 'treatment'
>>>>>>> 08759e2 (tests)
        })
    assert(res.status_code == 201)

    res = testapp.post_json(
        '/in_vitro',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
<<<<<<< HEAD
            'post_differentiation_time_units': 'second'
=======
            'post_differentiation_time_units': 'second',
            'treatment': 'treatment'
>>>>>>> 08759e2 (tests)
        }, expect_errors=True)
    assert(res.status_code == 422)
