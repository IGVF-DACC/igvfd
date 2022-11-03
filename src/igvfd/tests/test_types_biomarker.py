import pytest


def test_name_quantification_calculated_property(biomarker_CD243_absent, biomarker_CD243_high, testapp):
    res_bm_absent = testapp.get(biomarker_CD243_absent['@id'])
    assert res_bm_absent.json['name_quantification'] == 'CD243-'
    res_bm_high = testapp.get(biomarker_CD243_high['@id'])
    assert res_bm_high.json['name_quantification'] == 'CD243high'
