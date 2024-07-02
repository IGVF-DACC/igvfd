import pytest


def test_human_donor_summary(testapp, human_donor):
    res = testapp.get(human_donor['@id'])
    assert res.json.get('summary') == 'unspecified'

    testapp.patch_json(
        human_donor['@id'],
        {
            'ethnicities': ['Japanese'],
            'sex': 'male'
        }
    )
    res = testapp.get(human_donor['@id'])
    assert res.json.get('summary') == 'Japanese male'
