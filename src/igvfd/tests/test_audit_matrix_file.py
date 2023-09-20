import pytest


def test_audit_inconsistent_dimensions(
    testapp,
    matrix_file
):
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'dimension1': 'gene'
        }
    )
    assert any(
        error['category'] == 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
