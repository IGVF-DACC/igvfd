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
