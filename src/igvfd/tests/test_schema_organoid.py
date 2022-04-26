import pytest


def test_differentiation_dependency(organoid, testapp):
    res = testapp.patch_json(
        organoid['@id'],
        {'post_differentiation_time': 10}, expect_errors=True)
    assert(res.status_code == 422)

    res = testapp.patch_json(
        organoid['@id'],
        {'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert(res.status_code == 422)

    res = testapp.patch_json(
        organoid['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert(res.status_code == 200)


def test_post_organoid(testapp, award, lab, source):
    res = testapp.post_json(
        '/organoid',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': source['@id'],
            'post_differentiation_time': 72,
            'post_differentiation_time_units': 'hour',
            'treatment': 'treatment'
        })
    assert(res.status_code == 201)

    res = testapp.post_json(
        '/organoid',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'treatment': 'treatment'
        }, expect_errors=True)
    assert(res.status_code == 422)
