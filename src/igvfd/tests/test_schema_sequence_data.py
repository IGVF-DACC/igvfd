import pytest


def test_sequence_data_1(testapp, sequence_data):
    res = testapp.get(sequence_data['@id'])
    assert res.json['accession'][:6] == 'IGVFFF'


def test_sequence_data_validation_error_detail(testapp, sequence_data):
    res = testapp.patch_json(
        sequence_data['@id'],
        {'validation_error_detail': 'This is a comment.'},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_data['@id'],
        {
            'validation_error_detail': 'This is a comment.',
            'upload_status': 'invalidated'

        }
    )
    assert res.status_code == 200


def test_sequence_data_min_max_mean_read_length(testapp, sequence_data_fastq_no_read_length):
    res = testapp.post_json(
        '/sequence_data',
        sequence_data_fastq_no_read_length,
        expect_errors=True)
    assert res.status_code == 422

    sequence_data_fastq_no_read_length.update(
        {
            'minimum_read_length': 99,
            'maximum_read_length': 101,
            'mean_read_length': 100,
        }
    )
    res = testapp.post_json(
        '/sequence_data',
        sequence_data_fastq_no_read_length)
    assert res.status_code == 201


def test_sequence_data_dbxrefs_regex(testapp, sequence_data):
    res = testapp.patch_json(
        sequence_data['@id'],
        {'dbxrefs': [12345]},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_data['@id'],
        {'dbxrefs': ['not_a_sra_ID']},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_data['@id'],
        {'dbxrefs': ['SRA:SRR21927294', 'SRA:SRX21927294']}
    )
    assert res.status_code == 200
