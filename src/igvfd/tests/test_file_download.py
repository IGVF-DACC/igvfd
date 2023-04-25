import pytest


def test_file_download_has_uploading_file_credentials(testapp, sequence_file):
    assert 'upload_credentials' in sequence_file
    accession = sequence_file['accession']
    assert sequence_file['href'] == f'/sequence-files/{accession}/@@download/{accession}.fastq.gz'
    response = testapp.patch_json(
        sequence_file['@id'],
        {
            'upload_status': 'validated'
        }
    )
    updated_sequence_file = response.json['@graph'][0]
    assert 'upload_credentials' not in updated_sequence_file


def test_file_download_view_redirect(testapp, sequence_file):
    response = testapp.get(
        sequence_file['href'],
        extra_environ={
            'HTTP_X_FORWARDED_FOR': '100.100.100.100'
        }
    )
    assert '307 Temporary Redirect' in str(response.body)
    assert 'X-Accel-Redirect' not in response.headers
    assert 'http://localstack:4566/igvf-files-local' in response.headers['Location']


def test_file_download_view_proxy_range(testapp, sequence_file):
    response = testapp.get(
        sequence_file['href'],
        headers={
            'Range': 'bytes=0-4444'
        },
        extra_environ={
            'HTTP_X_FORWARDED_FOR': '100.100.100.100'
        },
    )
    assert '307 Temporary Redirect' in str(response.body)
    assert 'X-Accel-Redirect' not in response.headers


def test_file_download_view_soft_redirect(testapp, sequence_file):
    response = testapp.get(
        sequence_file['href'] + '?soft=True'
    )
    assert response.json['@type'][0] == 'SoftRedirect'
    assert 'location' in response.json


def test_file_download_regenerating_credentials_uploading_file_not_found(testapp, sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    properties = item.upgrade_properties()
    # Clear the external sheet.
    item.update(
        properties,
        sheets={
            'external': {},
        }
    )
    testapp.post_json(
        sequence_file['@id'] + '@@upload',
        {},
        status=404
    )


def test_file_download_file_not_found(testapp, sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    properties = item.upgrade_properties()
    # Clear the external sheet.
    item.update(
        properties,
        sheets={
            'external': {}
        }
    )
    testapp.get(
        sequence_file['href'],
        status=404
    )
