import pytest


def test_audit_missing_file_format_specifications(
    testapp,
    tabular_file,
    experimental_protocol_document
):
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {'file_format': 'vcf',
         'assembly': 'custom'}
    )
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {'file_format_specifications': [experimental_protocol_document['@id']],
         'file_format': 'tsv'}
    )
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing file format specifications'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
