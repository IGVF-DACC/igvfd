import pytest


def test_audit_primary_cell_age(
    testapp,
    sequence_file
):
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent seqspec metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
