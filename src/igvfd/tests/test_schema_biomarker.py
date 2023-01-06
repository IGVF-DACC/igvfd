import pytest


def test_biomarker_name_quantification_id(biomarker_CD243_absent, biomarker_CD1e_low, biomarker_IgA_present, primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'biomarker': [biomarker_CD243_absent['@id'], biomarker_CD1e_low['@id'], biomarker_IgA_present['@id']]})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'biomarker': [biomarker_CD243_absent['name_quantification'], biomarker_CD1e_low['name_quantification'], biomarker_IgA_present['name_quantification']]})
    assert res.status_code == 200


def test_biomarker_patch_synonym(biomarker_CD243_absent, testapp):
    res = testapp.patch_json(
        biomarker_CD243_absent['@id'],
        {'synonym': ['my marker synonym', 'another synonym', 'third synonym']})
    assert res.status_code == 200


def test_biomarker_check_duplicate(testapp, lab, award):
    my_duplicate_biomarker = {
        'name': 'CD1',
        'quantification': 'negative',
        'classification': 'cell surface protein',
        'award': award['@id'],
        'lab': lab['@id']
    }
    biomarker_CD1 = testapp.post_json('/biomarker', my_duplicate_biomarker, status=201).json['@graph'][0]
    res = testapp.post_json('/biomarker', my_duplicate_biomarker, status=409)
    assert res.status_code == 409


def test_biomarker_patch_gene(biomarker_CD1e_low, gene_CD1E, testapp):
    res = testapp.patch_json(
        biomarker_CD1e_low['@id'],
        {'gene': gene_CD1E['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        biomarker_CD1e_low['@id'],
        {'gene': 'ABC12345'},
        expect_errors=True)
    assert res.status_code == 422


def test_biomarker_permissions(submitter_testapp, testapp, lab, award):
    my_non_dacc_biomarker = {
        'name': 'CD1234',
        'quantification': 'negative',
        'classification': 'cell surface protein',
        'award': award['@id'],
        'lab': lab['@id']
    }
    res = submitter_testapp.post_json('/biomarker', my_non_dacc_biomarker, status=422)
    assert res.status_code == 422
    res = testapp.post_json('/biomarker', my_non_dacc_biomarker)
    assert res.status_code == 201


def test_biomarker_classifications(testapp, gene_myc_hs, lab, award):
    my_cell_surface_protein_biomarker = {
        'name': 'CD2345',
        'quantification': 'negative',
        'classification': 'cell surface protein',
        'award': award['@id'],
        'lab': lab['@id']
    }
    res = testapp.post_json('/biomarker', my_cell_surface_protein_biomarker)
    assert res.status_code == 201
    my_gene_marker_biomarker = {
        'name': 'MYC',
        'quantification': 'negative',
        'classification': 'marker gene',
        'gene': gene_myc_hs['@id'],
        'award': award['@id'],
        'lab': lab['@id']
    }
    res = testapp.post_json('/biomarker', my_gene_marker_biomarker)
    assert res.status_code == 201


def test_biomarker_alias_unique(biomarker_CD1e_low, biomarker_CD243_high, testapp):
    res = testapp.patch_json(
        biomarker_CD1e_low['@id'],
        {'alias': biomarker_CD243_high['alias']},
        expect_errors=True)
    assert res.status_code == 409
