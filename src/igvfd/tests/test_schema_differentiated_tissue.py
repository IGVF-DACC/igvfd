import pytest


def test_post_differentiated_tissue(testapp, award, lab, source, treatment_1, human_donor):
    res = testapp.post_json(
        '/differentiated_tissue',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': source['@id'],
            'post_differentiation_time': 72,
            'post_differentiation_time_units': 'hour',
            'treatments': [treatment_1['@id']],
            'taxa': 'Homo sapiens',
            'donors': [human_donor['@id']]
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


def test_part_of_tissue(differentiated_tissue, differentiated_tissue_part_of, differentiated_cell, testapp):
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'part_of': differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'part_of': differentiated_tissue_part_of['@id']})
    assert res.status_code == 200


def test_differentiation_time(differentiated_tissue, testapp):
    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'post_differentiation_time': 10}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'hour'}, expect_errors=True)
    assert res.status_code == 200

    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'stage'}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_tissue['@id'],
        {'post_differentiation_time': 10.2341, 'post_differentiation_time_units': 'minute'}, expect_errors=True)
    assert res.status_code == 200
