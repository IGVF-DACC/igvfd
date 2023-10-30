import pytest


def test_summary(testapp, primary_cell, pooled_from_primary_cell, human_donor, rodent_donor, parent_rodent_donor_2, biomarker_CD243_absent, biomarker_CD243_high, sample_term_endothelial_cell, treatment_protein, phenotype_term_myocardial_infarction, phenotype_term_alzheimers):
    res = testapp.get(primary_cell['@id'])
    assert res.json.get('summary') == 'pluripotent stem cell, Homo sapiens'
    testapp.patch_json(
        human_donor['@id'],
        {
            'sex': 'female',
        }
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'lower_bound_age': 1,
            'upper_bound_age': 3,
            'age_units': 'week'
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert res.json.get('summary') == 'pluripotent stem cell, female, Homo sapiens (1-3 weeks)'
    testapp.patch_json(
        primary_cell['@id'],
        {
            'lower_bound_age': 1,
            'upper_bound_age': 1,
            'age_units': 'month',
            'cellular_sub_pool': 'PKR-123',
            'virtual': True,
            'embryonic': True,
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert res.json.get(
        'summary') == 'virtual embryonic pluripotent stem cell (PKR-123), female, Homo sapiens (1 month)'
    testapp.patch_json(
        primary_cell['@id'],
        {
            'sample_terms': [sample_term_endothelial_cell['@id']],
            'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD243_high['@id']]
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert res.json.get(
        'summary') == 'virtual embryonic endothelial cell of vascular tree (PKR-123), female, Homo sapiens (1 month) characterized by high level of CD243, negative detection of CD243'
    testapp.patch_json(
        primary_cell['@id'],
        {
            'donors': [human_donor['@id'], rodent_donor['@id']],
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert res.json.get(
        'summary') == 'virtual embryonic endothelial cell of vascular tree (PKR-123), mixed sex, Homo sapiens and Mus musculus strain1 (1 month) characterized by high level of CD243, negative detection of CD243'
    testapp.patch_json(
        rodent_donor['@id'],
        {
            'sex': 'female',
        }
    )
    testapp.patch_json(
        parent_rodent_donor_2['@id'],
        {
            'sex': 'male',
        }
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'donors': [rodent_donor['@id'], parent_rodent_donor_2['@id']],
            'treatments': [treatment_protein['@id']],
            'disease_terms': [phenotype_term_myocardial_infarction['@id'], phenotype_term_alzheimers['@id']],
            'sorted_from': pooled_from_primary_cell['@id'],
            'sorted_from_detail': 'some more details about sorting'
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert res.json.get(
        'summary') == f'virtual embryonic endothelial cell of vascular tree (PKR-123), mixed sex, Mus musculus strain1, strain3 (1 month) (sorting details: some more details about sorting) characterized by high level of CD243, negative detection of CD243, associated with Alzheimer\'s disease, Myocardial infarction, treated with 10 ng/mL G-CSF'
