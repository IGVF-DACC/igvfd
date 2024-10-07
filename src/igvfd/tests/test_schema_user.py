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


def test_schema_user_no_uppercase_emails(testapp, verified_member):
    assert verified_member['email'].islower()
    testapp.patch_json(
        verified_member['@id'],
        {
            'email': 'new_email@some_domain.com'
        },
        status=200,
    )
    testapp.patch_json(
        verified_member['@id'],
        {
            'email': 'NEW_EMAIL@some_domain.com'
        },
        status=422,
    )
    testapp.patch_json(
        verified_member['@id'],
        {
            'email': 'NEW_EMAIL@SOME.DOMAIN.EDU.COM'
        },
        status=422,
    )
    testapp.patch_json(
        verified_member['@id'],
        {
            'email': 'new_email@some.domain.edu.coM'
        },
        status=422,
    )
    testapp.patch_json(
        verified_member['@id'],
        {
            'email': 'new_email@some.domain.edu.com'
        },
        status=200,
    )
