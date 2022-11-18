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
        {'synonyms': ['my marker synonym', 'another synonym', 'third synonym']})
    assert res.status_code == 200


def test_biomarker_check_duplicate(testapp):
    my_duplicate_biomarker = {
        'name': 'CD1',
        'quantification': 'negative',
        'classification': 'cell surface protein'
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


def test_biomarker_permissions(submitter_testapp, testapp):
    my_non_dacc_biomarker = {
        'name': 'CD1234',
        'quantification': 'negative',
        'classification': 'cell surface protein'
    }
    res = submitter_testapp.post_json('/biomarker', my_non_dacc_biomarker, status=422)
    assert res.status_code == 422
    res = testapp.post_json('/biomarker', my_non_dacc_biomarker)
    assert res.status_code == 201
