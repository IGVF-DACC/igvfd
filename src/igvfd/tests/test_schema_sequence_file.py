import pytest


def test_sequence_file_1(testapp, sequence_file):
    res = testapp.get(sequence_file['@id'])
    assert res.json['accession'][:6] == 'IGVFFI'


def test_sequence_file_validation_error_detail(testapp, sequence_file):
    res = testapp.patch_json(
        sequence_file['@id'],
        {'validation_error_detail': 'This is a comment.'},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'validation_error_detail': 'This is a comment.',
            'upload_status': 'invalidated'

        }
    )
    assert res.status_code == 200


def test_sequence_file_min_max_mean_read_length(testapp, sequence_file_fastq_no_read_length):
    # Validated fastqs must have read length and read count. Validated files must have file size.
    sequence_file_fastq_no_read_length.update(
        {
            'upload_status': 'validated'
        }
    )
    res = testapp.post_json(
        '/sequence_file',
        sequence_file_fastq_no_read_length,
        expect_errors=True)
    assert res.status_code == 422

    sequence_file_fastq_no_read_length.update(
        {
            'minimum_read_length': 99,
            'maximum_read_length': 101,
            'mean_read_length': 100,
            'read_count': 12081930,
            'file_size': 6743021
        }
    )
    res = testapp.post_json(
        '/sequence_file',
        sequence_file_fastq_no_read_length)
    assert res.status_code == 201


def test_sequence_file_dbxrefs_regex(testapp, sequence_file):
    res = testapp.patch_json(
        sequence_file['@id'],
        {'dbxrefs': [12345]},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_file['@id'],
        {'dbxrefs': ['not_a_sra_ID']},
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_file['@id'],
        {'dbxrefs': ['SRA:SRR21927294', 'SRA:SRX21927294']}
    )
    assert res.status_code == 200


def test_sequence_file_sequencing_run_uniqueness(
    testapp,
    sequence_file,
    sequence_file_sequencing_run_2
):
    # If there is no illumina_read_type, there cannot be 2 files with the same sequencing run in a given dataset.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {'sequencing_run': 1},
        expect_errors=True
    )
    assert res.status_code == 409

    # If the files are in different sequencing_runs, there is no clash.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {'sequencing_run': 2}
    )
    assert res.status_code == 200

    # If there is illumina_read_type, the combination of illumina_read_type and sequencing_run must be unique.
    res = testapp.patch_json(
        sequence_file['@id'],
        {'illumina_read_type': 'R1'}
    )

    # If both files are R1, there is a clash.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R1'
        },
        expect_errors=True
    )
    assert res.status_code == 409

    # If the files are different read types in the same sequencing run, there is no clash.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R2'
        }
    )
    assert res.status_code == 200
