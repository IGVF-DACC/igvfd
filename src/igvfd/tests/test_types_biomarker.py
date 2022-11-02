import pytest


def test_name_quantification_calculated_property(biomarker_absent, biomarker_high, testapp):
    res_bm_absent = testapp.get(biomarker_absent['@id'])
    assert res_bm_absent.json['name_quantification'] == 'CD243-'
    res_bm_high = testapp.get(biomarker_high['@id'])
    assert res_bm_high.json['name_quantification'] == 'CD243high'
