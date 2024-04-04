import pytest


def test_types_file_get_external_sheet(sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    actual = item._get_external_sheet()
    expected = {
        'key': '2023/01/21/8513c860-0e63-4e95-9459-f17a8f6ad45d/IGVFFF598NQZ.fastq.gz',
        'bucket': 'igvf-files-local',
        'service': 's3',
        'upload_credentials': {
            'access_key': 'AKIAIOSFODNN7EXAMPLE',
            'expiration': '2023-01-22T12:52:06.074000+00:00',
            'request_id': 'W36V9TIIUQGMWOX46LZHLLHDTG8U6HAONL18PGZLFOVLH5EQDEDO',
            'secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY',
            'upload_url': 's3://igvf-files-local/2023/01/21/8513c860-0e63-4e95-9459-f17a8f6ad45d/IGVFFF598NQZ.fastq.gz',
            'session_token': 'AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22wDOk4x4HIZ8j4FZTwdQWLWsKWHGBuFqwAeMicRXmxfpSPfIeoIYRqTflfKD8YUuwthAx7mSEI/qkPpKPi/kMcGdQrmGdeehM4IC1NtBmUpp2wUE8phUZampKsburEDy0KPkyQDYwT7WZ0wq5VSXDvp75YU9HFvlRd8Tx6q6fE8YQcHNVXAkiY9q6d+xo0rKwT38xVqr7ZD0u0iPPkUL64lIZbqBAz+scqKmlzm8FDrypNC9Yjc8fPOLn9FX9KSYvKTr4rvx3iSIlTJabIQwj2ICCR/oLxBA==',
            'federated_user_id': '000000000000:up1674262326.067452-IGVFFF598NQZ',
            'federated_user_arn': 'arn:aws:sts::000000000000:federated-user/up1674262326.067452-IGVFFF598NQZ'
        }
    }
    for key in ['key', 'bucket', 'service', 'upload_credentials']:
        assert key in actual
    for key in expected['upload_credentials']:
        assert key in actual['upload_credentials']
    for key in ['bucket', 'service']:
        assert actual[key] == expected[key]


def test_types_file_set_external_sheet(sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    external_to_set = {'bucket': 'new_test_file_bucket', 'key': 'abc.bam'}
    item._set_external_sheet(
        external_to_set
    )
    actual = item._get_external_sheet()
    expected = {
        'key': 'abc.bam',
        'bucket': 'new_test_file_bucket',
        'service': 's3',
    }
    for k, v in expected.items():
        assert actual[k] == v


def test_types_file_s3_uri_is_present(sequence_file):
    assert 's3_uri' in sequence_file


def test_types_file_s3_uri_non_submittable(testapp, analysis_set_with_sample, award, lab):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'minimum_read_length': 99,
        'maximum_read_length': 101,
        'mean_read_length': 100,
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'reads',
        'sequencing_run': 1,
        's3_uri': 's3://foo/bar/baz.fastq.gz'
    }
    testapp.post_json('/sequence_file/', item, status=422)


def test_types_aligment_file_content_summary(testapp, alignment_file):
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('content_summary') == 'unfiltered alignments'
    testapp.patch_json(
        alignment_file['@id'],
        {
            'redacted': True,
            'filtered': True
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('content_summary') == 'filtered redacted alignments'


def test_types_signal_file_content_summary(testapp, signal_file):
    res = testapp.get(signal_file['@id'])
    assert res.json.get('content_summary') == 'plus strand signal of all reads'
    testapp.patch_json(
        signal_file['@id'],
        {
            'filtered': True,
            'normalized': True,
            'strand_specificity': 'unstranded'
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('content_summary') == 'filtered normalized unstranded signal of all reads'


def test_types_matrix_file_content_summary(testapp, matrix_file):
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('content_summary') == 'cell by gene sparse gene count matrix'
    testapp.patch_json(
        matrix_file['@id'],
        {
            'dimension1': 'variant',
            'dimension2': 'treatment',
            'content_type': 'transcriptome annotations'
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('content_summary') == 'variant by treatment transcriptome annotations'


def test_integrated_in(testapp, construct_library_set_genome_wide, base_expression_construct_library_set, tabular_file):
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {
            'integrated_content_files': [tabular_file['@id']]
        }
    )
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'integrated_content_files': [tabular_file['@id']]
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert set(res.json.get('integrated_in')) == {
        base_expression_construct_library_set['@id'], construct_library_set_genome_wide['@id']}


def test_types_aligment_file_controlled_access(testapp, alignment_file):
    # Assert not controlled access has s3uri/href.
    res = testapp.get(alignment_file['@id'])
    assert not res.json.get('controlled_access')
    assert 's3_uri' in res.json
    assert 'href' in res.json

    # Assert upload/download works for not controlled access.
    res = testapp.get(alignment_file['@id'] + '@@upload')
    assert 'upload_credentials' in res.json['@graph'][0]
    testapp.post_json(alignment_file['@id'] + '@@upload', {}, status=200)
    testapp.get(alignment_file['@id'] + '@@download', status=307)

    # Assert controlled_access requireds anvil_source_url.
    res = testapp.patch_json(
        alignment_file['@id'],
        {
            'controlled_access': True
        }, expect_errors=True)
    assert res.status_code == 422

    # Switch to controlled access.
    res = testapp.patch_json(
        alignment_file['@id'],
        {
            'controlled_access': True,
            'anvil_source_url': 'https://lze1ablob.core.windows.net/sc-0f7a85e-9aeff8/SomeFile.fasta.gz'
        })
    assert res.status_code == 200

    # Assert controlled access doesn't have s3uri/href. Does have generated anvil_destination_url'
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('controlled_access') is True
    assert 's3_uri' not in res.json
    assert 'href' not in res.json
    assert 'anvil_destination_url' in res.json
    assert 'anvil_source_url' in res.json
    # Calculated path depends on workspace, creation date, uuid, accession, e.g.:
    # https://lze1a071f63dcb29ba120b05.blob.core.windows.net/sc-7d3c9ef1-99c2-4948-9811-fe79d626219f/2024/04/04/e55d6d97-f123-462b-8991-4d112d079a41/IGVFFI0968GYLL.bam
    assert res.json.get('anvil_destination_url').startswith(
        'https://lze1a071f63dcb29ba120b05.blob.core.windows.net/sc-7d3c9ef1-99c2-4948-9811-fe79d626219f/')
    assert res.json.get('anvil_destination_url').endswith(f'/{res.json.get("uuid")}/{res.json.get("accession")}.bam')

    # Assert upload/download fails for controlled access.
    testapp.get(alignment_file['@id'] + '@@upload', status=403)
    testapp.post_json(alignment_file['@id'] + '@@upload', {}, status=403)
    testapp.get(alignment_file['@id'] + '@@download', status=403)
