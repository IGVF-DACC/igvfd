import pytest


def test_biomarker_name_quantification_id(biomarker_CD243_absent, biomarker_CD1e_low, biomarker_IgA_present, primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'biomarkers': [biomarker_CD243_absent['@id'], biomarker_CD1e_low['@id'], biomarker_IgA_present['@id']]})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'biomarkers': [biomarker_CD243_absent['name_quantification'], biomarker_CD1e_low['name_quantification'], biomarker_IgA_present['name_quantification']]})
    assert res.status_code == 200


def test_biomarker_patch_synonim(biomarker_CD243_absent, biomarker_CD1e_low, testapp):
    res = testapp.patch_json(
        biomarker_CD243_absent['@id'],
        {'synonyms': ['my marker synonym', 'another synonym', 'third synonym']})
    assert res.status_code == 200


def test_biomarker_check_duplicate(testapp):
    my_duplicate_biomarker = {
        'name': 'CD1',
        'quantification': '-',
        'classification': 'cell surface protein'
    }
    biomarker_CD1 = testapp.post_json('/biomarker', my_duplicate_biomarker, status=201).json['@graph'][0]
    res = testapp.post_json('/biomarker', my_duplicate_biomarker, status=409)
    assert res.status_code == 409
