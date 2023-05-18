import pytest


def test_audit_primary_cell_age(
    testapp,
    primary_cell
):
    res = testapp.get(primary_cell['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing age properties'
        for error in res.json['audit'].get('WARNING', [])
    )
