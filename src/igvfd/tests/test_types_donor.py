import pytest


def test_superseded_by(testapp, human_donor, rodent_donor):
    testapp.patch_json(
        human_donor['@id'],
        {
            'supersedes': [rodent_donor['@id']]
        }
    )
    res = testapp.get(rodent_donor['@id'])
    assert set([donor for donor in res.json.get('superseded_by')]) == {rodent_donor['@id']}
