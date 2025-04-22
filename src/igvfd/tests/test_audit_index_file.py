import pytest


def test_audit_index_files(testapp, reference_file, index_file_tbi, tabular_file_bed):
    res = testapp.get(index_file_tbi['@id'] + '@@audit')
    assert all(
        audit['category'] != 'unexpected indexed file'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        index_file_tbi['@id'],
        {
            'derived_from': [reference_file['@id']]
        }
    )
    res = testapp.get(index_file_tbi['@id'] + '@@audit')
    assert any(
        audit['category'] == 'unexpected indexed file'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        index_file_tbi['@id'],
        {
            'derived_from': [tabular_file_bed['@id']]
        }
    )
    res = testapp.get(index_file_tbi['@id'] + '@@audit')
    assert all(
        audit['category'] != 'unexpected indexed file'
        for audit in res.json['audit'].get('ERROR', {})
    )
