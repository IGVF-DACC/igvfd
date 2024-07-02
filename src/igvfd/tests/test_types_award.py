import pytest


def test_award_summary(testapp, award):
    res = testapp.get(award['@id'])
    assert res.json.get('summary', '') == 'A Generic IGVF Award'
