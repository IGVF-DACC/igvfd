import pytest


def test_source_summary(testapp, source):
    res = testapp.get(source['@id'])
    assert res.json.get('summary', '') == 'Sigma-Aldrich'
