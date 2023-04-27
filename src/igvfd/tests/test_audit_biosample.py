import pytest


def test_audit_biosample_nih_institutional_certification(
    testapp,
    primary_cell
):
    res = testapp.get(primary_cell['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing nih_institutional_certification'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'nih_institutional_certification': 'NIC00042'
        }
    )
    res = testapp.get(primary_cell['@id'] + '@@index-data')
    assert all(
        error['category'] != 'missing nih_institutional_certification'
        for error in res.json['audit'].get('ERROR', [])
    )
