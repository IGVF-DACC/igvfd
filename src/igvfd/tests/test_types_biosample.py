import pytest


def test_tissue_sex_calculation(testapp, tissue, human_donor):
    res = testapp.get(tissue['@id'])
    assert(not res.json.get('sex'))
    res = testapp.patch_json(
        tissue['@id'],
        {'donors': [human_donor['@id']]})
    res = testapp.get(tissue['@id'])
    assert(not res.json.get('sex'))
    res = testapp.patch_json(
        human_donor['@id'],
        {'sex': 'female'})
    res = testapp.get(tissue['@id'])
    assert(res.json.get('sex') == 'female')
