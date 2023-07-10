import pytest
import json


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
    terms_set = set()
    terms_set.add(tissue.get('biosample_term', None))
    terms_set.add(in_vitro_cell_line.get('biosample_term', None))
    multiplexed_term_set = set([entry['@id'] for entry in res.json.get('biosample_terms', [])])
    assert terms_set == multiplexed_term_set

    diseases_set = set()
    diseases_set.add(phenotype_term_myocardial_infarction['@id'])
    multiplexed_diseases_set = set([entry['@id'] for entry in res.json.get('disease_terms', [])])
    assert diseases_set == multiplexed_diseases_set

    modifications_set = set()
    modifications_set.add(modification['@id'])
    multiplexed_modifications_set = set([entry for entry in res.json.get('modifications', [])])
    assert modifications_set == multiplexed_modifications_set

    donors_set = set()
    donors_set.update(tissue.get('donors', []))
    donors_set.update(in_vitro_cell_line.get('donors', []))
    multiplexed_donors_set = set([entry for entry in res.json.get('donors', [])])
    assert donors_set == multiplexed_donors_set

    biomarkers_set = set()
    biomarkers_set.add(biomarker_CD243_absent['@id'])
    biomarkers_set.add(biomarker_CD1e_low['@id'])
    biomarkers_set.add(biomarker_IgA_present['@id'])
    multiplexed_biomarkers_set = set([entry for entry in res.json.get('biomarkers', [])])
    assert biomarkers_set == multiplexed_biomarkers_set

    res = testapp.get(tissue['@id'])
    assert res.json.get('multiplexed_in') == [multiplexed_sample['@id']]
