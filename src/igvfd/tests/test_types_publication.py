import pytest


def test_publication_year(testapp, publication):
    res = testapp.patch_json(
        publication['@id'],
        {'date_published': '2022-09-13'}).json['@graph'][0]
    assert res['publication_year'] == 2022
