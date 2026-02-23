import pytest


def test_audit_tissue_age(
    testapp,
    tissue
):
    res = testapp.get(tissue['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing age'
        for error in res.json['audit'].get('WARNING', [])
    )
