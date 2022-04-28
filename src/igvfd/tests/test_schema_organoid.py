import pytest


def test_post_organoid(testapp, award, lab, source):
    res = testapp.post_json(
        '/organoid',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': source['@id'],
            'post_differentiation_time': 72,
            'post_differentiation_time_units': 'hour',
            'treatments': ['treatment']
        })
    assert(res.status_code == 201)

    res = testapp.post_json(
        '/organoid',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'treatments': ['treatment']
        }, expect_errors=True)
    assert(res.status_code == 422)
