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


def test_summary(testapp, in_vitro_cell_line, technical_sample, sample_term_endothelial_cell, sample_term_embryoid_body, sample_term_lymphoblastoid, sample_term_brown_adipose_tissue, treatment_chemical):
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'K562 cell line, Mus musculus (100 hours)'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
            'time_post_change': 10,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_chemical['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'lymphoblastoid cell line, Mus musculus (10 minutes)'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_endothelial_cell['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'day',
            'cell_fate_change_treatments': [treatment_chemical['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'endothelial cell line of vascular tree, Mus musculus (5 days)'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_embryoid_body['@id']],
            'classification': 'embryoid',
            'time_post_change': 3,
            'time_post_change_units': 'week',
            'cell_fate_change_treatments': [treatment_chemical['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'embryoid body, Mus musculus (3 weeks)'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_brown_adipose_tissue['@id']],
            'classification': 'organoid',
            'time_post_change': 1,
            'time_post_change_units': 'month',
            'cell_fate_change_treatments': [treatment_chemical['@id']],
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'brown adipose tissue organoid, Mus musculus (1 month)'
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'synthetic technical sample'


def test_summary_mixed_taxa(testapp, in_vitro_cell_line, human_donor, rodent_donor, treatment_chemical):
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'donors': [human_donor['@id'], rodent_donor['@id']],
            'time_post_change': 1,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_chemical['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'K562 cell line (1 minute)'


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
