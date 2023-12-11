import pytest
import os


def test_upload_credentials_init_s3_upload_credentials():
    from igvfd.upload_credentials import get_sts_client
    from igvfd.upload_credentials import S3UploadCredentials
    upload_credentials = S3UploadCredentials(
        bucket='some-bucket',
        key='some-key',
        name='some-name',
        sts_client=get_sts_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        )
    )
    assert isinstance(upload_credentials, S3UploadCredentials)


def test_upload_credentials_init_gcs_upload_credentials():
    pass


def test_upload_credentials_s3_upload_credentials_external_credentials():
    from igvfd.upload_credentials import get_sts_client
    from igvfd.upload_credentials import S3UploadCredentials
    upload_credentials = S3UploadCredentials(
        bucket='some-bucket',
        key='some-key',
        name='some-name',
        sts_client=get_sts_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        )
    )
    actual = upload_credentials.external_creds()
    expected = {
        'service': 's3',
        'bucket': 'some-bucket',
        'key': 'some-key',
        'upload_credentials': {
            'session_token': 'AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22wDOk4x4HIZ8j4FZTwdQWLWsKWHGBuFqwAeMicRXmxfpSPfIeoIYRqTflfKD8YUuwthAx7mSEI/qkPpKPi/kMcGdQrmGdeehM4IC1NtBmUpp2wUE8phUZampKsburEDy0KPkyQDYwT7WZ0wq5VSXDvp75YU9HFvlRd8Tx6q6fE8YQcHNVXAkiY9q6d+xo0rKwT38xVqr7ZD0u0iPPkUL64lIZbqBAz+scqKmlzm8FDrypNC9Yjc8fPOLn9FX9KSYvKTr4rvx3iSIlTJabIQwj2ICCR/oLxBA==',
            'access_key': 'AKIAIOSFODNN7EXAMPLE',
            'expiration': '2023-01-22T11:54:30.557000+00:00',
            'secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY',
            'upload_url': 's3://some-bucket/some-key',
            'federated_user_arn': 'arn:aws:sts::000000000000:federated-user/some-name',
            'federated_user_id': '000000000000:some-name',
            'request_id':
            'NJSHEOGY4R9JSD87SKWL51KTLL9TVP6QSQ0TSEFA4RVD65RGS2ZL'
        }
    }
    for key in ['service', 'bucket', 'key']:
        assert actual[key] == expected[key]
    for key in expected['upload_credentials']:
        assert key in actual['upload_credentials']
    assert actual['upload_credentials']['upload_url'] == 's3://some-bucket/some-key'


def test_upload_credentials_gcs_upload_credentials_external_credentials():
    pass
