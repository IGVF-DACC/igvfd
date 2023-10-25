import pytest


def test_passage_number_dependency(in_vitro_cell_line, testapp):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'passage_number': 3})
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'classification': 'differentiated cell'}, expect_errors=True)
    assert res.status_code == 422


def test_time_post_factors_dependency(in_vitro_cell_line, treatment_chemical, testapp):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'time_post_change': 3}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'cell_fate_change_treatments': [treatment_chemical['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'time_post_change': 3, 'time_post_change_units': 'day', 'cell_fate_change_treatments': [treatment_chemical['@id']]})
    assert res.status_code == 200


def test_sorted_from(testapp, in_vitro_organoid, in_vitro_differentiated_cell):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_from': in_vitro_organoid['@id'],
         'sorted_from_detail': 'default test description'})
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'sorted_from': 'I am just pretending to be a sorted fraction parent.',
         'sorted_from_detail': 'default test description'}, expect_errors=True)
    assert res.status_code == 422


def test_sorted_fraction_detail_dependency(testapp, in_vitro_organoid, primary_cell):
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_from': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_from_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'sorted_from': primary_cell['@id'],
         'sorted_from_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200


def test_cellular_sub_pool(testapp, in_vitro_differentiated_cell, primary_cell, in_vitro_organoid):
    res = testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {'cellular_sub_pool': 'SS-PKR_1'}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'cellular_sub_pool': 'SS-PKR_1'}, expect_errors=True)
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_organoid['@id'],
        {'cellular_sub_pool': 'LW231B-2'}, expect_errors=True)


def test_classification_dependency(testapp, lab, award, source, human_donor, sample_term_K562, treatment_chemical, in_vitro_cell_line, sample_term_brown_adipose_tissue):
    item = {
        'classification': 'differentiated cell specimen',
        'award': award['@id'],
        'lab': lab['@id'],
        'sources': [source['@id']],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'sample_terms': [sample_term_K562['@id']],
        'cell_fate_change_treatments': [treatment_chemical['@id']],
        'time_post_change': 5,
        'time_post_change_units': 'minute'
    }
    res = testapp.post_json('/in_vitro_system', item, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'classification': 'organoid',
            'cell_fate_change_treatments': [treatment_chemical['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'classification': 'organoid',
            'cell_fate_change_treatments': [treatment_chemical['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id']
        })
    assert res.status_code == 200


def test_in_vitro_system_submitter(submitter_testapp, in_vitro_system_sub):
    submitter_testapp.post_json('/in_vitro_system?render=False', in_vitro_system_sub, status=201)


def test_maxitems_dependencies(in_vitro_cell_line, modification, modification_activation,
                               source, source_lonza, assay_term_starr, assay_term_atac, testapp):
    # Sources, modifications, and sample_terms arrays should only have 1 entry
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'modifications': [modification['@id']]})
    assert res.status_code == 200
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'modifications': [modification['@id'], modification_activation['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'sources': [source['@id'], source_lonza['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'sample_terms': [assay_term_starr['@id'], assay_term_atac['@id']]}, expect_errors=True)
    assert res.status_code == 422


def test_sample_moi_construct_library(
    testapp,
    in_vitro_cell_line,
    construct_library_set_genome_wide
):
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'moi': 2.1},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'moi': 2.1,
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    assert res.status_code == 200
