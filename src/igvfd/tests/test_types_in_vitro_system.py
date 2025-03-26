import pytest


def test_summary(testapp, in_vitro_cell_line, in_vitro_differentiated_cell, human_donor, rodent_donor, biomarker_CD243_absent, biomarker_CD243_high, sample_term_lymphoblastoid, sample_term_endothelial_cell, sample_term_embryoid_body, sample_term_brown_adipose_tissue, sample_term_gastrula, treatment_protein, depletion_treatment, construct_library_set_reporter, crispr_modification):
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('summary') == 'Mus musculus strain1 (male) K562 cell line'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
            'time_post_change': 10,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_protein['@id']]
        }
    )
    res = testapp.get(in_vitro_differentiated_cell['@id'])
    assert res.json.get(
        'summary') == 'Homo sapiens lymphoblastoid differentiated cell specimen line induced to brown adipose tissue for 10 minutes'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'day',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id']
        }
    )
    res = testapp.get(in_vitro_differentiated_cell['@id'])
    assert res.json.get(
        'summary') == 'Homo sapiens lymphoblastoid differentiated cell specimen line induced to endothelial cell of vascular tree for 5 days'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_brown_adipose_tissue['@id']],
            'classifications': ['organoid'],
            'time_post_change': 1,
            'time_post_change_units': 'month',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_lymphoblastoid['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'Mus musculus strain1 (male) brown adipose tissue organoid induced to lymphoblastoid cell line for 1 month'
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
        'summary') == 'Homo sapiens and Mus musculus strain1 (mixed sex) brown adipose tissue organoid induced to brown adipose tissue for 5 minutes'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_embryoid_body['@id']],
            'classifications': ['embryoid'],
            'time_post_change': 3,
            'time_post_change_units': 'week',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'treatments': [depletion_treatment['@id'], treatment_protein['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id'],
            'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD243_high['@id']],
            'sorted_from': in_vitro_differentiated_cell['@id'],
            'sorted_from_detail': 'some detail about sorting',
            'virtual': True,
            'cellular_sub_pool': 'PKR-456',
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == f'virtual Homo sapiens and Mus musculus strain1 (mixed sex) embryoid body induced to endothelial cell of vascular tree for 3 weeks (cellular sub pool: PKR-456) (sorting details: some detail about sorting) characterized by high level of CD243, negative detection of CD243, depleted of penicillin for 3 minutes, treated with 10 ng/mL G-CSF'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'donors': [human_donor['@id'], rodent_donor['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id'],
            'modifications': [crispr_modification['@id']],
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'virtual Homo sapiens and Mus musculus strain1 (mixed sex) embryoid body induced to brown adipose tissue for 5 minutes (cellular sub pool: PKR-456) (sorting details: some detail about sorting) characterized by high level of CD243, negative detection of CD243, depleted of penicillin for 3 minutes, treated with 10 ng/mL G-CSF, modified with CRISPRi Sp-dCas9, transfected with a reporter library'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'moi': 2,
            'nucleic_acid_delivery': 'transfection',
            'construct_library_sets': [construct_library_set_reporter['@id']],
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id'],
            'time_post_change_units': 'minute'
        }
    )
    res = testapp.get(in_vitro_differentiated_cell['@id'])
    assert res.json.get(
        'summary') == 'Homo sapiens lymphoblastoid differentiated cell specimen line induced to brown adipose tissue for 5 minutes transfected with a reporter library (MOI of 2)'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'growth_medium': 'DMEM with serum',
            'biosample_qualifiers': ['exhausted']
        }
    )
    res = testapp.get(in_vitro_differentiated_cell['@id'])
    assert res.json.get(
        'summary') == 'Homo sapiens exhausted lymphoblastoid differentiated cell specimen line induced to brown adipose tissue for 5 minutes transfected with a reporter library (MOI of 2), grown in DMEM with serum'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'time_post_library_delivery': 7,
            'time_post_library_delivery_units': 'day'
        }
    )
    res = testapp.get(in_vitro_differentiated_cell['@id'])
    assert res.json.get(
        'summary') == 'Homo sapiens exhausted lymphoblastoid differentiated cell specimen line induced to brown adipose tissue for 5 minutes 7 day(s) after transfection with a reporter library (MOI of 2), grown in DMEM with serum'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'classifications': ['gastruloid'],
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'cell_fate_change_treatments': [treatment_protein['@id']],
            'targeted_sample_term': sample_term_gastrula['@id'],
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get(
        'summary') == 'virtual Homo sapiens and Mus musculus strain1 (mixed sex) embryoid body induced to gastrula for 5 minutes (cellular sub pool: PKR-456) (sorting details: some detail about sorting) characterized by high level of CD243, negative detection of CD243, depleted of penicillin for 3 minutes, treated with 10 ng/mL G-CSF, modified with CRISPRi Sp-dCas9, transfected with a reporter library'
