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


def test_post_in_vitro(testapp, award, lab):
    res = testapp.post_json(
        '/in_vitro',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'minute',
            'treatment': 'treatment'
        })
    assert(res.status_code == 201)

    res = testapp.post_json(
        '/in_vitro',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'second',
            'treatment': 'treatment'
        }, expect_errors=True)
    assert(res.status_code == 422)
