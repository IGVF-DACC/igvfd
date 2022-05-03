import pytest


def test_post_organoid(testapp, award, lab, source, treatment_1):
    res = testapp.post_json(
        '/organoid',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': source['@id'],
            'post_differentiation_time': 72,
            'post_differentiation_time_units': 'hour',
            'treatments': [treatment_1['@id']]
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


def test_organoid_age_unit_dependency(organoid, testapp):
    res = testapp.patch_json(
        organoid['@id'],
        {'organism': 'Saccharomyces', 'age_units': 'minute'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        organoid['@id'],
        {'age_units': 'month'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        organoid['@id'],
        {'organism': 'Homo sapiens', 'age_units': 'minute'}, expect_errors=True)
    assert(res.status_code == 422)
