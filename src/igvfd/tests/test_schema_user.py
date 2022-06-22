import pytest


def test_job_title(testapp, pi):
    res = testapp.patch_json(
        pi['@id'],
        {'job_title': 'PI'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        pi['@id'],
        {'job_title': 'Principal Investigator'})
    assert res.status_code == 200
