import pytest


def test_audit_treatment_id(testapp, treatment_ntr):
    res = testapp.get(treatment_ntr['@id'] + '@@index-data')
    assert any(
        error['category'] == 'treatment term has been newly requested'
        for error in res.json['audit'].get('WARNING', [])
    )
