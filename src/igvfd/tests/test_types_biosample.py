import pytest


def test_tissue_sex_calculation(testapp, tissue, human_donor, human_male_donor):
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id']], 'taxa': 'Homo sapiens'})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') == 'unspecified'
    res = testapp.patch_json(
        human_donor['@id'],
        {'sex': 'female'})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') == 'female'
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id'], human_male_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') == 'mixed'


def test_age_calculation(testapp, cell_line):
    res = testapp.get(cell_line['@id'])
    assert res.json.get('age') == 'unknown'
    res = testapp.patch_json(
        cell_line['@id'],
        {'lower_bound_age': 10, 'upper_bound_age': 10, 'age_units': 'year'})
    res = testapp.get(cell_line['@id'])
    assert res.json.get('age') == '10'
    res = testapp.patch_json(
        cell_line['@id'],
        {'upper_bound_age': 15})
    res = testapp.get(cell_line['@id'])
    assert res.json.get('age') == '10-15'
    res = testapp.patch_json(
        cell_line['@id'],
        {'lower_bound_age': 90, 'upper_bound_age': 90, 'age_units': 'year'})
    res = testapp.get(cell_line['@id'])
    print(res.json.get('age'))
    assert res.json.get('age') == '90 or above'
    res = testapp.patch_json(
        cell_line['@id'],
        {'age_units': 'month'})
    res = testapp.get(cell_line['@id'])
    assert res.json.get('age') == '90'
