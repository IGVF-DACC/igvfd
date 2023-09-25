import pytest


def test_audit_identical_dimensions(
    testapp,
    matrix_file
):
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'identical dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'dimension1': 'gene'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'identical dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
