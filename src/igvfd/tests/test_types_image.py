import pytest


def test_summary(testapp, image):
    res = testapp.get(image['@id'])
    uuid = res.json.get('uuid')
    assert uuid == res.json.get('summary')
    testapp.patch_json(
        image['@id'],
        {'caption': 'A red dot.'}
    )
    res = testapp.get(image['@id'])
    assert res.json.get('summary') == 'A red dot.'
