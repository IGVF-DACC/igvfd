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


def test_unique_identifiers(publication, testapp):
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['PMID:1000', 'doi:10.1000/100']})
    assert res.status_code == 200
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['doi:10.1000/100', 'doi:10.1000/100']}, expect_errors=True)
    assert res.status_code == 422


def test_required_properties(award, lab, testapp):
    res = testapp.post_json(
        '/publication',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'title': 'Publication'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/publication',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'identifiers': ['PMID:1000']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/publication',
        {
            'award': award['@id'],
            'title': 'Publication',
            'identifiers': ['PMID:1000']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/publication',
        {
            'lab': lab['@id'],
            'title': 'Publication',
            'identifiers': ['PMID:1000']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/publication',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'title': 'Publication',
            'identifiers': ['PMID:1000']
        })
    assert res.status_code == 201


def test_identifier_pattern(publication, testapp):
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['PMCID:PMC3439153']})
    assert res.status_code == 200
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['PMID:21765801']})
    assert res.status_code == 200
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['doi:10.1038/nphys1170']})
    assert res.status_code == 200
    res = testapp.patch_json(
        publication['@id'],
        {'identifiers': ['doi:9.1038/nphys1170']}, expect_errors=True)
    assert res.status_code == 422
