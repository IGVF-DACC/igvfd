import pytest


def test_audit_missing_file_format_specifications_model_file(
    testapp,
    model_file,
    experimental_protocol_document
):
    res = testapp.get(model_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        model_file['@id'],
        {'file_format_specifications': [experimental_protocol_document['@id']]}
    )
    res = testapp.get(model_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
