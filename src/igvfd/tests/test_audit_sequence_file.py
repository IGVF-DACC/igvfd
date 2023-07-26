import pytest


def test_audit_inconsistent_seqspec(
    testapp,
    sequence_file
):
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent seqspec metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
