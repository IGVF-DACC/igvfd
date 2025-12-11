import pytest


def test_audit_upload_status(testapp, reference_file, model_file, external_lab):
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
            'lab': external_lab['@id']
        },
        status=200,
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert all(
        audit['category'] == 'upload status not validated'
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
        for audit in res.json['audit'].get('ERROR', {})
    )
    # No audit for externally hosted files.
    testapp.patch_json(
        model_file['@id'],
        {
            'upload_status': 'pending'
        },
        status=200,
    )
    res = testapp.get(model_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'upload status not validated'
        for audit in res.json['audit'].get('ERROR', {})
    )
    testapp.patch_json(
        model_file['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'https://external_host.com/'
        },
        status=200,
    )
    res = testapp.get(model_file['@id'] + '@@audit')
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


def test_audit_external_reference_files(testapp, reference_file, external_lab):
    # Use external lab name as the replacement of 'external' field.
    testapp.patch_json(
        reference_file['@id'],
        {
            'lab': external_lab['@id'],

        }
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'missing dbxrefs'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
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
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
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


def test_audit_file_mixed_assembly_transcriptome_annotation(testapp, matrix_file, reference_file_with_assembly, reference_file_with_transcriptome):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'reference_files': [reference_file_with_assembly['@id'], reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'inconsistent transcriptome annotation'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
    testapp.patch_json(
        reference_file_with_assembly['@id'],
        {
            'assembly': 'GRCm39'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'inconsistent transcriptome annotation'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
    testapp.patch_json(
        reference_file_with_transcriptome['@id'],
        {
            'assembly': 'GRCh38',
            'content_type': 'genome reference'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'mixed assembly'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )
    testapp.patch_json(
        reference_file_with_transcriptome['@id'],
        {
            'content_type': 'transcriptome reference'
        }
    )
    testapp.patch_json(
        reference_file_with_assembly['@id'],
        {
            'content_type': 'transcriptome reference',
            'transcriptome_annotation': 'GENCODE M34'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'mixed transcriptome annotation'
        for audit in res.json['audit'].get('NOT_COMPLIANT', {})
    )


def test_audit_public_file_in_private_bucket(testapp, dummy_request, signal_file_with_external_sheet):
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-05-31T12:34:56Z',
            'upload_status': 'validated',

        }
    )
    res = testapp.get(signal_file_with_external_sheet['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = [error for v in errors.values() for error in v if error['category'] == 'incorrect file bucket']
    assert errors_list
    assert errors_list[0]['detail'].split('to')[-1].strip() == 's3://igvf-public-local/xyz.bigWig'
    res = testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'igvf-public-local',
        }
    )
    res = testapp.get(signal_file_with_external_sheet['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = [error for v in errors.values() for error in v if error['category'] == 'incorrect file bucket']
    assert not errors_list


def test_audit_private_file_in_public_bucket(testapp, dummy_request, signal_file_with_external_sheet):
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'status': 'deleted',
            'upload_status': 'validated',
        }
    )
    res = testapp.get(signal_file_with_external_sheet['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = [error for v in errors.values() for error in v]
    assert errors_list
    assert errors_list[0]['detail'].split('to')[-1].strip() == 's3://igvf-private-local/xyz.bigWig'


def test_audit_file_statuses_in_s3_statuses(testapp):
    # Make sure public_s3_statuses and private_s3_statuses lists in File item include
    # all statuses in File schema, except upload failed and content error.
    from igvfd.types.file import File
    public_s3_statuses = File.public_s3_statuses
    private_s3_statuses = File.private_s3_statuses
    assert public_s3_statuses
    assert private_s3_statuses
    file_schema = testapp.get('/profiles/sequence_file.json').json
    file_statuses = file_schema.get('properties', {}).get('status', {}).get('enum')
    assert file_statuses
    # If this fails sync public/private_s3_statuses with statuses in file schema.
    assert not set(file_statuses) - set(public_s3_statuses + private_s3_statuses)


def test_audit_supersedes(testapp, reference_file, tabular_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'supersedes': [tabular_file['@id']]

        }
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'status': 'deleted'
        }
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert any(
        audit['category'] == 'inconsistent superseding'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'status': 'archived',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
            'file_size': 5000,
            'md5sum': '51ff37ad73d8f3d7c3fa2d7f6fd5073b',
            'submitted_file_name': 'sometabfile.tsv'
        }
    )
    res = testapp.get(reference_file['@id'] + '@@audit')
    assert all(
        audit['category'] != 'inconsistent superseding'
        for audit in res.json['audit'].get('INTERNAL_ACTION', {})
    )


def test_audit_cell_annotation_without_marker_file(testapp, matrix_file, tabular_file, experimental_protocol_document, document_pipeline_parameters):
    # Setup: make it into a cell marker file
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'cell marker file'
        }
    )

    # Check native audit on matrix file without cell annotation file
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch Matrix File content type and check for audit
    testapp.patch_json(
        matrix_file['@id'],
        {
            'content_type': 'annotated sparse gene count matrix'
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch an unrelated document and check audit still raises missing cell marker file
    testapp.patch_json(
        matrix_file['@id'],
        {
            'documents': [document_pipeline_parameters['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch the cell marker file to Matrix File and check audit clears
    testapp.patch_json(
        matrix_file['@id'],
        {
            'documents': [experimental_protocol_document['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Check native audit on tabular file without cell annotation file
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch Tabular File content type and check for audit
    testapp.patch_json(
        tabular_file['@id'],
        {
            'content_type': 'cell annotations'
        }
    )
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch an unrelated document and check audit still raises missing cell marker file
    testapp.patch_json(
        tabular_file['@id'],
        {
            'documents': [document_pipeline_parameters['@id']]
        }
    )
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )

    # Patch the cell marker file to Tabular File and check audit clears
    testapp.patch_json(
        tabular_file['@id'],
        {
            'documents': [experimental_protocol_document['@id']]
        }
    )
    res = testapp.get(tabular_file['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing cell marker file'
        for error in res.json['audit'].get('WARNING', {})
    )
