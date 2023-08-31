import pytest


def test_summary(testapp, in_vitro_cell_line, in_vitro_differentiated_cell, human_donor, rodent_donor, biomarker_CD243_absent, biomarker_CD243_high, sample_term_lymphoblastoid, sample_term_endothelial_cell, sample_term_embryoid_body, sample_term_brown_adipose_tissue, treatment_protein):
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'K562 cell line, male Mus musculus strain1'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
            'time_post_change': 10,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_protein['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'lymphoblastoid cell line induced for 10 minutes, male Mus musculus strain1'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'day',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'lymphoblastoid cell line induced to endothelial cell of vascular tree for 5 days, male Mus musculus strain1'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_brown_adipose_tissue['@id']],
            'classification': 'organoid',
            'time_post_change': 1,
            'time_post_change_units': 'month',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_lymphoblastoid['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'brown adipose tissue organoid induced to lymphoblastoid cell line for 1 month, male Mus musculus strain1'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'donors': [human_donor['@id'], rodent_donor['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'brown adipose tissue organoid induced to brown adipose tissue for 5 minutes, mixed sex'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_embryoid_body['@id']],
            'classification': 'embryoid',
            'time_post_change': 3,
            'time_post_change_units': 'week',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id'],
            'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD243_high['@id']],
            'sorted_fraction': in_vitro_differentiated_cell['@id'],
            'sorted_fraction_detail': 'some detail about sorting'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    treatment_summary = testapp.get(treatment_protein['@id']).json.get('title')
    treatment_summary = treatment_summary.replace('Treatment of', 'treated with')
    assert res.json.get(
        'summary') == f'embryoid body induced to endothelial cell of vascular tree for 3 weeks, mixed sex (sorting details: some detail about sorting) characterized by high level of CD243, negative detection of CD243 {treatment_summary}'
