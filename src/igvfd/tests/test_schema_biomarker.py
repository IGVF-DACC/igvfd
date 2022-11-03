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
