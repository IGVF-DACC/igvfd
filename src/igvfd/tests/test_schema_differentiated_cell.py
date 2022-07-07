import pytest


def test_differentiation_dependency(differentiated_cell, testapp):
    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'post_differentiation_time': 10}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert res.status_code == 200


def test_post_differentiated_cell(testapp, award, lab, treatment_2, human_donor):
    res = testapp.post_json(
        '/differentiated_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'minute',
            'treatments': [treatment_2['@id']],
            'taxa': 'Homo sapiens',
            'donors': [human_donor['@id']]
        })
    assert res.status_code == 201

    res = testapp.post_json(
        '/differentiated_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'second'
        }, expect_errors=True)
    assert res.status_code == 422
