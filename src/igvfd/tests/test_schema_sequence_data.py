import pytest


def test_file_1(testapp, sequence_data):
    res = testapp.get(sequence_data['@id'])
    assert res.json['accession'][:6] == 'IGVFFF'


def test_file_validation_error_detail(testapp, sequence_data):
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


def test_file_paired_with(testapp, sequence_data, sequence_data_paired_end_1):
    # Paired_end requires run_type
    res = testapp.patch_json(
        sequence_data['@id'],
        {'paired_end': '2'},
        expect_errors=True
    )
    assert res.status_code == 422

    # Paired_end and paired_with are not applicable to single-ended fastqs.
    res = testapp.patch_json(
        sequence_data['@id'],
        {
            'run_type': 'single-ended',
            'paired_end': '1'
        },
        expect_errors=True
    )
    assert res.status_code == 422

    # A paired-end 2 file must be paired_with some other file.
    res = testapp.patch_json(
        sequence_data['@id'],
        {
            'run_type': 'paired-ended',
            'paired_end': '2'
        },
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        sequence_data['@id'],
        {
            'run_type': 'paired-ended',
            'paired_end': '2',
            'paired_with': sequence_data_paired_end_1['@id']
        }
    )
    assert res.status_code == 200
