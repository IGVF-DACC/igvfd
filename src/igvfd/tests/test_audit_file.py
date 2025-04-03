import pytest


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
        audit['category'] == 'upload status not validated'
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
        audit['category'] == 'upload status not validated'
        for audit in res.json['audit'].get('WARNING', {})
    )
    assert all(
        audit['category'] != 'upload status not validated'
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
        audit['category'] != 'upload status not validated'
        for audit in res.json['audit'].get('WARNING', {})
    )
    assert all(
        audit['category'] != 'upload status not validated'
        for audit in res.json['audit'].get('ERROR', {})
    )
    # No audit for validation exempted either.
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'validation exempted'

        },
        status=200,
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'upload status not validated'
        for audit in res.json['audit'].get('WARNING', {})
    )
    assert all(
        audit['category'] != 'upload status not validated'
        for audit in res.json['audit'].get('ERROR', {})
    )


def test_audit_file_format_specifications(testapp, matrix_file, experimental_protocol_document):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_format_specifications': [experimental_protocol_document['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'inconsistent document type'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'file format specification'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'inconsistent document type'
        for audit in res.json['audit'].get('ERROR', {})
    )


def test_audit_external_reference_files(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'external': True
        }
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'missing dbxrefs'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'dbxrefs': ['ENCODE:ENCFF743WOO']
        }
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'missing dbxrefs'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )


def test_audit_multiple_seqspec_per_seqfile(testapp, sequence_file, configuration_file_seqspec, configuration_file_seqspec_2):
    # Patch 1 seqspec files to the basic seq_file and new status as in progress (no audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'status': 'in progress'
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'unexpected seqspecs'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )
    # Patch 2 seqspec files to the basic seq_file and new status as in progress (internal_action)
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'status': 'in progress'
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'unexpected seqspecs'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )
    # Patch 1 seqspec files to the basic seq_file and new status as released (no audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
            'file_size': 5003,
            'md5sum': 'ddbbb36d7b3aac3477d3ecf87ddf865f',
            'submitted_file_name': 'local/config_file_seqspec.yaml'
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'unexpected seqspecs'
        for audit in res.json['audit'].get('ERROR', {})
    )
    # Patch 2 seqspec files to the basic seq_file and new status as released (Error)
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
            'file_size': 5000,
            'md5sum': '51ff37ad73d8f3d7c3fa2d7f6fd5073a',
            'submitted_file_name': 'local/config_file_seqspec_2.yaml'
        }
    )
    res = testapp.get(sequence_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'unexpected seqspecs'
        for audit in res.json['audit'].get('ERROR', {})
    )
