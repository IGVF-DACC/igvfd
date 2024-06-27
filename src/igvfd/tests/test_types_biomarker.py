import pytest


def test_name_quantification_calculated_property(biomarker_CD243_absent, biomarker_CD243_high, testapp):
    res_bm_absent = testapp.get(biomarker_CD243_absent['@id'])
    assert res_bm_absent.json['name_quantification'] == 'CD243-negative'
    res_bm_high = testapp.get(biomarker_CD243_high['@id'])
    assert res_bm_high.json['name_quantification'] == 'CD243-high'


def test_biomarker_for(testapp, in_vitro_system_v20, biomarker_v2):
    testapp.patch_json(
        in_vitro_system_v20['@id'],
        {
            'biomarkers': [biomarker_v2['@id']]
        }
    )
    res = testapp.get(biomarker_v2['@id'])
    assert res.json.get('biomarker_for', []) == [in_vitro_system_v20['@id']]
