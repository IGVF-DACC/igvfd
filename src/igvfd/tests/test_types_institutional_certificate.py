import pytest


def test_types_institutional_certificate_summary(testapp, institutional_certificate):
    res = testapp.get(institutional_certificate['@id'])
    assert res.json.get('summary') == f'{institutional_certificate["certificate_identifier"]} (unrestricted)'
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'controlled_access': 'true'
        }
    )
    res = testapp.get(institutional_certificate['@id'])
    assert res.json.get('summary') == f'{institutional_certificate["certificate_identifier"]} (controlled)'
