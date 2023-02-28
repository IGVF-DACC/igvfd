import pytest


def test_passage_number_dependency(in_vitro_cell_line, testapp):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'passage_number': 3})
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'classification': 'differentiated cell'}, expect_errors=True)
    assert res.status_code == 422


def test_time_post_factors_dependency(in_vitro_differentiated_cell, testapp):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'time_post_factors_introduction': 3, 'time_post_factors_introduction_units': 'day'}, expect_errors=True)
    assert res.status_code == 200


def test_sorted_fraction(testapp, lab, award, source, human_donor, sample_term_K562):
    item_1 = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    source_cell = testapp.post_json('/in_vitro_system', item_1, status=201).json['@graph'][0]
    item_2 = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id'],
        'sorted_fraction': source_cell['@id']
    }
    res = testapp.post_json('/in_vitro_system', item_2, status=201)
    assert res.status_code == 201
    item_3 = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id'],
        'sorted_fraction': 'I am just pretending to be a sorted fraction.'
    }
    res = testapp.post_json('/in_vitro_system', item_3, status=422)
    assert res.status_code == 422
