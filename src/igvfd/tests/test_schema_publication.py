import pytest


def test_date_published(publication, testapp):
    res = testapp.patch_json(
        publication['@id'],
        {'date_published': '2022-2-2'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        publication['@id'],
        {'date_published': '2022-02-02'})
    assert res.status_code == 200
