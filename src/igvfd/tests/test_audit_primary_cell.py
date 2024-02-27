import pytest


def test_audit_primary_cell_age(
    testapp,
    primary_cell
):
    res = testapp.get(primary_cell['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing age'
        for error in res.json['audit'].get('WARNING', [])
    )
