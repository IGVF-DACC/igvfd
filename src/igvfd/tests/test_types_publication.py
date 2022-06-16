import pytest


def test_publication_year(testapp, publication):
    res = testapp.patch_json(
        publication['@id'],
        {'date_published': '2012-09-06'})
    assert publication['Publication year'] == '2012'
