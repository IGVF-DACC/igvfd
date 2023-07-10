import pytest


def test_file_sets_link(testapp, tissue, measurement_set, analysis_set_base, curated_set_genome):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(tissue['@id'])
    assert res.json.get('file_sets') == [measurement_set['@id']]
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(tissue['@id'])
    assert set(res.json.get('file_sets')) == {
        measurement_set['@id'], analysis_set_base['@id'], curated_set_genome['@id']}


def test_multiplexed_sample_props(
        testapp, multiplexed_sample, tissue, modification, in_vitro_cell_line,
        phenotype_term_myocardial_infarction, biomarker_CD243_absent,
        biomarker_CD1e_low, biomarker_IgA_present):
    res = testapp.get(multiplexed_sample['@id'])
    assert len(res.json.get('biosample_terms')) == 2
    testapp.patch_json(
        tissue['@id'],
        {
            'disease_terms': [phenotype_term_myocardial_infarction['@id']],
            'modification': modification['@id'],
            'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD1e_low['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'modification': modification['@id'],
            'biomarkers': [biomarker_IgA_present['@id'], biomarker_CD1e_low['@id']]
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get('disease_terms')[0]['term_name'] == 'Myocardial infarction'
    assert len(res.json.get('modifications')) == 1
    assert len(res.json.get('donors')) == 1
    assert len(res.json.get('biomarkers')) == 3
    res = testapp.get(tissue['@id'])
    assert len(res.json.get('multiplexed_in')) == 1
