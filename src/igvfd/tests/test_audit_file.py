import pytest


def test_audit_file_controlled_access_file_in_correct_anvil_workspace(testapp, alignment_file):
    res = testapp.get(alignment_file['@id'])
    assert res.json['upload_status'] == 'pending'
    assert res.json['controlled_access'] is False
    res = testapp.get(alignment_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'incorrect anvil workspace'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'controlled_access': True,
            'anvil_source_url': 'https://lze1ablob.core.windows.net/sc-0f7a85e-9aeff8/SomeFile.fasta.gz'
        },
        status=200,
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json['upload_status'] == 'pending'
    assert res.json['controlled_access'] is True
    assert 'anvil_destination_url' in res.json
    res = testapp.get(alignment_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'incorrect anvil workspace'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'upload_status': 'deposited'
        },
        status=200,
    )
    res = testapp.get(alignment_file['@id'] + '@@audit')
    assert not any(
        audit['category'] == 'incorrect anvil workspace'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )


def test_audit_upload_status(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'pending'
        },
        status=200,
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'unvalidated upload status'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'invalidated',
            'external': True
        },
        status=200,
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'unvalidated upload status'
        for audit in res.json['audit'].get('WARNING', {})
    )
    assert all(
        audit['category'] != 'unvalidated upload status'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'validated',
            'file_size': 123,

        },
        status=200,
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'unvalidated upload status'
        for audit in res.json['audit'].get('WARNING', {})
    )
    assert all(
        audit['category'] != 'unvalidated upload status'
        for audit in res.json['audit'].get('ERROR', {})
    )
