import pytest


def test_summary(testapp, image):
    res = testapp.get(image['@id'])
    caption = res.json.get('caption')
    assert caption == res.json.get('summary')
