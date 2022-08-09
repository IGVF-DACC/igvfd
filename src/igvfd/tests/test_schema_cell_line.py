import pytest


def test_sample_1(cell_line, testapp):
    res = testapp.get(cell_line['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_age_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'upper_bound_age': 1, 'lower_bound_age': 0}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line['@id'],
        {'lower_bound_age': 0, 'age_units': 'year'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line['@id'],
        {'upper_bound_age': 1, 'age_units': 'year'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line['@id'],
        {'upper_bound_age': 1, 'lower_bound_age': 0, 'age_units': 'year'})
    assert res.status_code == 200


def test_age_unit_dependency(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'taxa': 'Homo sapiens', 'lower_bound_age': 5, 'upper_bound_age': 10, 'age_units': 'year'})
    assert res.status_code == 200
    res = testapp.patch_json(
        cell_line['@id'],
        {'age_units': 'minute'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line['@id'],
        {'taxa': 'Saccharomyces'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line['@id'],
        {'taxa': 'Saccharomyces', 'age_units': 'minute'})
    assert res.status_code == 200


# def test_lifestage_dependency(cell_line, testapp):
#     res = testapp.patch_json(
#         cell_line['@id'],
#         {'taxa': 'Homo sapiens', 'life_stage': 'adult'})
#     assert res.status_code == 200
#     res = testapp.patch_json(
#         cell_line['@id'],
#         {'taxa': 'Mus musculus', 'life_stage': 'stationary'}, expect_errors=True)
#     assert res.status_code == 422
#     res = testapp.patch_json(
#         cell_line['@id'],
#         {'taxa': 'Saccharomyces', 'life_stage': 'adult'}, expect_errors=True)
#     assert res.status_code == 422


def test_nih_institutional_certification(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'nih_institutional_certification': 'NICHD1455'})
    assert res.status_code == 200
    res = testapp.patch_json(
        cell_line['@id'],
        {'nih_institutional_certification': 'ABBBCCCHD1455'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(cell_line, testapp):
    res = testapp.patch_json(
        cell_line['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        cell_line['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_date_format(cell_line_with_date_obtained, testapp):
    res = testapp.patch_json(
        cell_line_with_date_obtained['@id'],
        {'date_obtained': '2022-01-02'})
    assert res.status_code == 200
    res = testapp.patch_json(
        cell_line_with_date_obtained['@id'],
        {'date_obtained': '2022-05-10T22:09:05.876084+00:00'}, expect_errors=True)
    assert res.status_code == 422


def test_taxa_donors_requirements(testapp, award, lab, human_donor):
    res = testapp.post_json(
        '/cell_line',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
            'taxa': 'Homo sapiens',
            'donors': [human_donor['@id']]
        })
    assert res.status_code == 201

    res = testapp.post_json(
        '/cell_line',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'source': lab['@id'],
        }, expect_errors=True)
    assert res.status_code == 422


def test_part_of_cell_line(cell_line, cell_line_part_of, differentiated_cell, testapp):
    res = testapp.patch_json(
        cell_line_part_of['@id'],
        {'part_of': differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        cell_line_part_of['@id'],
        {'part_of': cell_line['@id']})
    assert res.status_code == 200
