import pytest


def test_post_differentiated_tissue(testapp, award, lab, source, treatment_1):
    res = testapp.post_json(
        '/differentiated_tissue',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': source['@id'],
            'post_differentiation_time': 72,
            'post_differentiation_time_units': 'hour',
            'treatments': [treatment_1['@id']]
        })
    assert res.status_code == 201

    res = testapp.post_json(
        '/differentiated_tissue',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'treatments': ['treatment']
        }, expect_errors=True)
    assert res.status_code == 422


def test_differentiated_tissue_age_unit_dependency(differentiated_tissue, testapp):
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'taxa': 'Saccharomyces', 'age': '5', 'age_units': 'minute'})
    assert res.status_code == 200
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'age_units': 'month'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'taxa': 'Homo sapiens', 'age_units': 'minute'}, expect_errors=True)
    assert res.status_code == 422
