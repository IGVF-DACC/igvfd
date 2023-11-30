import pytest


def test_transcriptome_annotation_dependency(testapp, reference_file):
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE M32'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE 40'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'GENCODE M30'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'GENCODE 40'
        }, expect_errors=True
    )
    assert res.status_code == 422


def test_schema_reference_file_validation_error_detail_only_allowed_when_upload_status_is_invalidated(testapp, reference_file):
    # Given a file with upload_status: pending:
    testapp.patch_json(reference_file['@id'], {'upload_status': 'pending'}, status=200)
    # When validation_error_details added, then patch fails:
    testapp.patch_json(
        reference_file['@id'],
        {
            'validation_error_detail': 'some problem with validating the file'
        },
        status=422
    )
    # Given a file with upload_status: invalidated:
    testapp.patch_json(reference_file['@id'], {'upload_status': 'invalidated'}, status=200)
    # When validation_error_details added, then patch works:
    testapp.patch_json(
        reference_file['@id'],
        {
            'validation_error_detail': 'some problem with validating the file'
        },
        status=200
    )


def test_schema_reference_file_must_remove_validation_error_detail_before_upload_status_changed_to_pending(testapp, reference_file):
    # Given a file with upload_status: invalidated and validation_error_detail:
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'invalidated',
            'validation_error_detail': 'some problem with validating the file'
        },
        status=200
    )
    # When upload_status changed to pending, then patch fails:
    testapp.patch_json(reference_file['@id'], {'upload_status': 'pending'}, status=422)
    # Given a file with validation_error_detail removed:
    r = testapp.get(reference_file['@id'] + '@@raw').json
    r.pop('validation_error_detail')
    testapp.put_json(reference_file['@id'], r, status=200)
    # When upload_status changed to pending, then patch works:
    testapp.patch_json(reference_file['@id'], {'upload_status': 'pending'}, status=200)


def test_schema_reference_file_regeneratiing_upload_credentials_leads_to_valid_schema(testapp, reference_file):
    # Given a file with upload_status: invalidated and validation_error_detail:
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'invalidated',
            'validation_error_detail': 'some problem with validating the file'
        },
        status=200
    )
    # When credentials are regenerated:
    r = testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)
    # Then the resulting JSON can be put back without validation error:
    r = testapp.get(reference_file['@id'] + '@@raw').json
    testapp.put_json(reference_file['@id'], r, status=200)


def test_schema_reference_file_regenerating_upload_credentials_fails_if_upload_status_is_validated(testapp, reference_file):
    # Given a file with upload_status: validated:
    testapp.patch_json(reference_file['@id'], {'upload_status': 'validated', 'file_size': 123}, status=200)
    # Then regenerating upload credentials fails:
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=403)


def test_schema_reference_file_regenerating_upload_credentials_on_invalid_file_clears_validation_error_details(testapp, reference_file):
    # Given a file with upload_status: invalidated and validation_error_detail:
    testapp.patch_json(
        reference_file['@id'],
        {
            'upload_status': 'invalidated',
            'validation_error_detail': 'some problem with validating the file'
        },
        status=200
    )
    # When credentials are regenerated:
    r = testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)
    # Then upload_status is pending and validation_error_details are removed:
    assert r.json['@graph'][0]['upload_status'] == 'pending'
    assert 'validation_error_detail' not in r.json['@graph'][0]
