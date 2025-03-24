import pytest


def test_types_institutional_certificate_summary(testapp, institutional_certificate_noncontrolled):
    res = testapp.get(institutional_certificate_noncontrolled['@id'])
    assert res.json.get(
        'summary') == f'{institutional_certificate_noncontrolled["certificate_identifier"]} (unrestricted)'
    testapp.patch_json(
        institutional_certificate_noncontrolled['@id'],
        {
            'controlled_access': 'true'
        }
    )
    res = testapp.get(institutional_certificate_noncontrolled['@id'])
    assert res.json.get(
        'summary') == f'{institutional_certificate_noncontrolled["certificate_identifier"]} (controlled)'
