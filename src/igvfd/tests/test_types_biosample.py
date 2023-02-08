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


def test_age_calculation(testapp, in_vitro_cell_line):
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('age') == 'unknown'
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'lower_bound_age': 10, 'upper_bound_age': 10, 'age_units': 'year'})
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('age') == '10'
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'upper_bound_age': 15})
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('age') == '10-15'
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'lower_bound_age': 90, 'upper_bound_age': 90, 'age_units': 'year'})
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('age') == '90 or above'
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'age_units': 'month'})
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('age') == '90'


def test_summary(testapp, tissue, primary_cell, whole_organism, in_vitro_cell_line):
    res = testapp.get(tissue['@id'])
    assert res.json.get('summary') == 'adrenal gland tissue, Mus musculus'
    res = testapp.patch_json(
        tissue['@id'],
        {'lower_bound_age': 10, 'upper_bound_age': 10, 'age_units': 'month'})
    res = testapp.get(tissue['@id'])
    assert res.json.get('summary') == 'adrenal gland tissue, Mus musculus, 10 month'

    res = testapp.get(primary_cell['@id'])
    assert res.json.get('summary') == 'pluripotent stem cell primary cell, Homo sapiens'
    res = testapp.patch_json(
        primary_cell['@id'],
        {'lower_bound_age': 1, 'upper_bound_age': 3, 'age_units': 'week'})
    res = testapp.get(primary_cell['@id'])
    assert res.json.get('summary') == 'pluripotent stem cell primary cell, Homo sapiens, 1-3 week'

    res = testapp.get(whole_organism['@id'])
    assert res.json.get('summary') == 'whole organism, Mus musculus'
    res = testapp.patch_json(
        whole_organism['@id'],
        {'lower_bound_age': 1, 'upper_bound_age': 1, 'age_units': 'hour'})
    res = testapp.get(whole_organism['@id'])
    assert res.json.get('summary') == 'whole organism, Mus musculus, 1 hour'

    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'K562 cell line, Mus musculus'
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'time_post_factors_introduction': 100, 'time_post_factors_introduction_units': 'hour'})
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'K562 cell line, Mus musculus (100 hour)'
