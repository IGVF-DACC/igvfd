import pytest


def test_tissue_sex_calculation(testapp, tissue, human_donor, human_male_donor):
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') in None
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') is None
    res = testapp.patch_json(
        human_donor['@id'],
        {'sex': 'female'})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') == 'female'
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id'], human_male_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert res.json.get('sex') == 'mixed'
