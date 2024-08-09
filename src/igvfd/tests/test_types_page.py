import pytest


def test_summary(testapp, page):
    res = testapp.get(page['@id'])
    title = res.json.get('title')
    assert title == res.json.get('summary')
