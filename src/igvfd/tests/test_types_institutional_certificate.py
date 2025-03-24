import pytest


def test_types_institutional_certificate_summary(testapp, institutional_certificate, institutional_certificate_controlled):
    res = testapp.get(institutional_certificate['@id'])
    assert res.json.get(
        'summary') == f'{institutional_certificate["certificate_identifier"]} (unrestricted)'
    res = testapp.get(institutional_certificate_controlled['@id'])
    assert res.json.get(
        'summary') == f'{institutional_certificate_controlled["certificate_identifier"]} (controlled)'
