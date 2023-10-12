import pytest


def test_tissue_sex_calculation(testapp, tissue, human_donor, human_male_donor):
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id']]})
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


def test_tissue_taxa_calculation(testapp, tissue, human_donor, rodent_donor):
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('taxa') == 'Homo sapiens'
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [rodent_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('taxa') == 'Mus musculus'
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id'], rodent_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('taxa', None) == None


def test_parent_of(testapp, primary_cell, tissue, in_vitro_cell_line):
    testapp.patch_json(
        primary_cell['@id'],
        {
            'part_of': tissue['@id']
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'part_of': tissue['@id']
        }
    )
    res = testapp.get(tissue['@id'])
    assert set(res.json.get('parent_of')) == {in_vitro_cell_line['@id'], primary_cell['@id']}


def test_pooled_in(testapp, primary_cell, tissue, in_vitro_cell_line):
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'pooled_from': [tissue['@id'], primary_cell['@id']]
        }
    )
    res = testapp.get(tissue['@id'])
    print(res.json.get('pooled_in'))
    assert res.json.get('pooled_in') == in_vitro_cell_line['@id']
