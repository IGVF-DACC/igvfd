import pytest


def test_human_donor_summary(testapp, human_donor):
    res = testapp.get(human_donor['@id'])
    assert res.json.get('summary') == res.json.get('uuid')

    testapp.patch_json(
        human_donor['@id'],
        {
            'ethnicities': ['Japanese'],
            'sex': 'male'
        }
    )
    res = testapp.get(human_donor['@id'])
    assert res.json.get('summary') == 'Japanese male'
    testapp.patch_json(
        human_donor['@id'],
        {
            'human_donor_identifers': ['AAA100']
        }
    )
    res = testapp.get(human_donor['@id'])
    assert res.json.get('summary') == 'Japanese male (AAA100)'
