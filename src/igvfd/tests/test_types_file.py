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

    res = testapp.patch_json(
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

    res = testapp.patch_json(
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
    assert res.json.get('content_summary') == 'cell by gene parse gene count matrix'
    res = testapp.patch_json(
        matrix_file['@id'],
        {
            'dimension1': 'variant',
            'dimension2': 'treatment',
            'strand_specificity': 'transcriptome annotations'
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('content_summary') == 'variant by treatment transcriptome annotations'
