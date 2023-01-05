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


def test_post_differentiated_cell(testapp, award, lab, treatment_protein,
                                  human_donor, sample_term_K562,
                                  sample_term_whole_organism):
    res = testapp.post_json(
        '/differentiated_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'minute',
            'treatments': [treatment_protein['@id']],
            'taxa': 'Homo sapiens',
            'donors': [human_donor['@id']],
            'biosample_term': sample_term_K562['@id'],
            'differentiation_origin': sample_term_whole_organism['@id']
        })
    assert res.status_code == 201

    res = testapp.post_json(
        '/differentiated_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'post_differentiation_time': 20,
            'post_differentiation_time_units': 'second',
        }, expect_errors=True)
    assert res.status_code == 422


def test_part_of_differentiated_cell(differentiated_cell, differentiated_cell_part_of, cell_line, testapp):
    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'part_of': cell_line['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'part_of': differentiated_cell_part_of['@id']})
    assert res.status_code == 200


def test_differentiation_time(differentiated_cell, testapp):
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
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'hour'})
    assert res.status_code == 200

    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'post_differentiation_time': 10, 'post_differentiation_time_units': 'stage'}, expect_errors=True)
    assert res.status_code == 422

    res = testapp.patch_json(
        differentiated_cell['@id'],
        {'post_differentiation_time': 10.2341, 'post_differentiation_time_units': 'minute'})
    assert res.status_code == 200
