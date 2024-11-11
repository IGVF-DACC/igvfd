import pytest


def test_audit_identical_dimensions(
    testapp,
    matrix_file,
    matrix_file_hic
):
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'principal_dimension': 'gene'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
    res = testapp.get(matrix_file_hic['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_format': 'cool'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('WARNING', [])
    )
