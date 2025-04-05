import pytest


def test_audit_external_identifiers(testapp, sequence_file):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'http://test_url'
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'missing dbxrefs'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'dbxrefs': ['SRA:SRR20474123']
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'missing dbxrefs'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
