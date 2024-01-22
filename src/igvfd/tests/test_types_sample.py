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
    f_id = []
    for f in res.json.get('file_sets'):
        f_id.append(f['@id'])
    assert f_id == [measurement_set['@id']]
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
    f_id = []
    for f in res.json.get('file_sets'):
        f_id.append(f['@id'])
    assert set(f_id) == {
        measurement_set['@id'], analysis_set_base['@id'], curated_set_genome['@id']}


def test_multiplexed_sample_props(
        testapp, multiplexed_sample, tissue, modification, in_vitro_cell_line,
        phenotype_term_myocardial_infarction, biomarker_CD243_absent,
        biomarker_CD1e_low, biomarker_IgA_present, construct_library_set_genome_wide,
        base_expression_construct_library_set, construct_library_set_reporter):
    testapp.patch_json(
        tissue['@id'],
        {
            'disease_terms': [phenotype_term_myocardial_infarction['@id']],
            'modifications': [modification['@id']],
            'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD1e_low['@id']],
            'construct_library_sets': [construct_library_set_genome_wide['@id'],
                                       base_expression_construct_library_set['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'modifications': [modification['@id']],
            'biomarkers': [biomarker_IgA_present['@id'], biomarker_CD1e_low['@id']],
            'construct_library_sets': [base_expression_construct_library_set['@id'], construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    terms_set = set()
    terms_set.update(tissue.get('sample_terms', []))
    terms_set.update(in_vitro_cell_line.get('sample_terms', []))
    multiplexed_term_set = set([entry['@id'] for entry in res.json.get('sample_terms', [])])
    assert terms_set == multiplexed_term_set

    diseases_set = set()
    diseases_set.add(phenotype_term_myocardial_infarction['@id'])
    multiplexed_diseases_set = set([entry['@id'] for entry in res.json.get('disease_terms', [])])
    assert diseases_set == multiplexed_diseases_set

    modifications_set = set()
    modifications_set.add(modification['@id'])
    multiplexed_modifications_set = []
    for m in res.json.get('modifications'):
        multiplexed_modifications_set.append(m['@id'])
    assert modifications_set == set(multiplexed_modifications_set)

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

    cls_set = set()
    cls_set.add(construct_library_set_genome_wide['@id'])
    cls_set.add(base_expression_construct_library_set['@id'])
    cls_set.add(construct_library_set_reporter['@id'])
    multiplexed_cls_set = set([entry['@id'] for entry in res.json.get('construct_library_sets', [])])
    assert cls_set == multiplexed_cls_set

    sources_set = set()
    sources_set.update(tissue.get('sources', []))
    sources_set.update(in_vitro_cell_line.get('sources', []))
    multiplexed_sources_set = set([entry['@id'] for entry in res.json.get('sources', [])])
    assert sources_set == multiplexed_sources_set
    res = testapp.get(tissue['@id'])
    multiplexed_in = []
    for m in res.json.get('multiplexed_in'):
        multiplexed_in.append(m['@id'])
    assert multiplexed_in == [multiplexed_sample['@id']]


def test_classifications(testapp, primary_cell, technical_sample, whole_organism, tissue, in_vitro_cell_line, multiplexed_sample):
    res = testapp.get(primary_cell['@id'])
    print(res)
    assert res.json.get('classifications') == ['primary cell']
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('classifications') == ['technical sample']
    res = testapp.get(whole_organism['@id'])
    assert res.json.get('classifications') == ['whole organism']
    res = testapp.get(tissue['@id'])
    assert res.json.get('classifications') == ['tissue']
    res = testapp.get(in_vitro_cell_line['@id'])
    assert res.json.get('classifications') == ['cell line']
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get('classifications') == ['multiplexed sample']


def test_sorted_fractions(testapp, primary_cell, tissue, in_vitro_cell_line):
    testapp.patch_json(
        tissue['@id'],
        {
            'sorted_from': primary_cell['@id'],
            'sorted_from_detail': 'something',
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sorted_from': primary_cell['@id'],
            'sorted_from_detail': 'something',
        }
    )
    res = testapp.get(primary_cell['@id'])
    assert set(res.json.get('sorted_fractions')) == {in_vitro_cell_line['@id'], tissue['@id']}


def test_origin_of(testapp, in_vitro_differentiated_cell, tissue, in_vitro_cell_line):
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'originated_from': tissue['@id'],
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'originated_from': tissue['@id'],
        }
    )
    res = testapp.get(tissue['@id'])
    assert set(res.json.get('origin_of')) == {in_vitro_cell_line['@id'], in_vitro_differentiated_cell['@id']}
