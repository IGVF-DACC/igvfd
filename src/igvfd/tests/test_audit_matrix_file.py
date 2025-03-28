import pytest


def test_audit_identical_dimensions(
    testapp,
    matrix_file,
    matrix_file_hic
):
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('ERROR', [])
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
        for error in res.json['audit'].get('ERROR', [])
    )
    res = testapp.get(matrix_file_hic['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent dimensions'
        for error in res.json['audit'].get('ERROR', [])
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
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_file_format_specifications_matrix_file(
    testapp,
    matrix_file,
    experimental_protocol_document
):
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {'file_format_specifications': [experimental_protocol_document['@id']]}
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
