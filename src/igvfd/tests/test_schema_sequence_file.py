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
    sequence_file_sequencing_run_2,
    sequence_file_pod5
):
    '''
    Properties combined to check for uniqueness:
    measurement_set, illumina_read_type, sequencing_run, flowcell_id, lane, index
    '''

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

    # If flowcell_id differs but all other properties match, there is no clash.
    testapp.patch_json(
        sequence_file['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R1',
            'lane': 1,
            'flowcell_id': 'FCX',
        }
    )
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R1',
            'lane': 1,
            'flowcell_id': 'FCX',

        },
        expect_errors=True
    )
    assert res.status_code == 409
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R1',
            'lane': 1,
            'flowcell_id': 'ABC',

        }
    )
    assert res.status_code == 200

    # If lane differs but all other properties match, there is no clash.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1,
            'illumina_read_type': 'R1',
            'lane': 2,
            'flowcell_id': 'FCX',

        }
    )
    assert res.status_code == 200

    # If the fastq has derived_from and is not released, there is
    # no unique key added.
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'derived_from': [sequence_file_pod5['@id']],
            'sequencing_run': 10
        }
    )
    assert res.status_code == 200

    # If the file is released and has derived from, then there
    # must not be any other released file.
    testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'released',
            'upload_status': 'validated',
            'release_timestamp': '2024-01-01T23:04:37.145369+00:00',
            'lane': 2
        }
    )
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'derived_from': [sequence_file_pod5['@id']],
            'sequencing_run': 10,
            'status': 'released',
            'upload_status': 'validated',
            'release_timestamp': '2024-01-01T23:04:37.145369+00:00',
        },
        expect_errors=True
    )
    assert res.status_code == 409

    # If the other file is not released, there is no clash.
    res = testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'derived_from': [sequence_file_pod5['@id']],
            'status': 'archived',
            'upload_status': 'validated',
            'release_timestamp': '2024-01-01T23:04:37.145369+00:00'
        }
    )
    assert res.status_code == 200


def test_sequence_file_upload_status(testapp, sequence_file):
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'file not found'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'pending'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'revoked',
            'upload_status': 'file not found',
            'release_timestamp': '2024-03-06T12:34:56Z',
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'revoked',
            'upload_status': 'pending',
            'release_timestamp': '2024-03-06T12:34:56Z',
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'archived',
            'upload_status': 'file not found',
            'release_timestamp': '2024-03-06T12:34:56Z',
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'archived',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'pending'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'validated'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-03-06T12:34:56Z',
            'upload_status': 'invalidated'
        }
    )
    assert res.status_code == 200


def test_sequence_file_content_type_file_format(testapp, sequence_file):
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'file_format': 'bam'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'content_type': 'Nanopore reads'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'content_type': 'PacBio subreads'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'file_format': 'bam',
            'content_type': 'PacBio subreads'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        sequence_file['@id'],
        {
            'file_format': 'pod5',
            'content_type': 'Nanopore reads'
        }
    )
    assert res.status_code == 200


def test_controlled_sequence_file_release(testapp, controlled_sequence_file_object):
    res = testapp.patch_json(
        controlled_sequence_file_object['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-05-31T12:34:56Z'
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        controlled_sequence_file_object['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-05-31T12:34:56Z',
            'anvil_source_url': 'http://abc.123'
        },
        expect_errors=True
    )
    assert res.status_code == 200
