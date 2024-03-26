import pytest


def test_audit_treatment_id(testapp, treatment_ntr):
    res = testapp.get(treatment_ntr['@id'] + '@@audit')
    assert any(
        error['category'] == 'NTR term ID'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
