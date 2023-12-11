import copy
import datetime
import json
import os

import boto3
import botocore

from botocore.client import BaseClient

from datetime import timedelta
from datetime import timezone

from google.api_core.exceptions import ClientError
from google.cloud import storage
from google.oauth2.service_account import Credentials

from typing import Optional


def get_secretsmanager_client():
    return boto3.client(
        'secretsmanager'
    )


def get_upload_files_user_access_key_and_secret_access_key():
    client = get_secretsmanager_client()
    return json.loads(
        client.get_secret_value(
            SecretId=os.environ['UPLOAD_USER_ACCESS_KEYS_SECRET_ARN']
        )['SecretString']
    )


def get_sts_client(localstack_endpoint_url: Optional[str] = None) -> BaseClient:
    if localstack_endpoint_url is not None:
        return boto3.client(
            'sts',
            endpoint_url=localstack_endpoint_url,
            aws_access_key_id='testing',
            aws_secret_access_key='testing',
            region_name='us-west-2',
        )
    upload_files_user_keys = get_upload_files_user_access_key_and_secret_access_key()
    return boto3.client(
        'sts',
        aws_access_key_id=upload_files_user_keys['ACCESS_KEY'],
        aws_secret_access_key=upload_files_user_keys['SECRET_ACCESS_KEY'],
        region_name='us-west-2',
    )


def get_s3_client(localstack_endpoint_url: Optional[str] = None) -> BaseClient:
    if localstack_endpoint_url is not None:
        return boto3.client(
            's3',
            endpoint_url=localstack_endpoint_url,
            aws_access_key_id='testing',
            aws_secret_access_key='testing',
            region_name='us-west-2',
        )
    return boto3.client(
        's3'
    )


def get_gcp_project():
    upload_files_user_keys = get_upload_files_user_access_key_and_secret_access_key()
    return upload_files_user_keys['GCP_PROJECT']


def get_gcp_service_account_json():
    upload_files_user_keys = get_upload_files_user_access_key_and_secret_access_key()
    return json.loads(
        upload_files_user_keys['GCP_SERVICE_ACCOUNT_JSON_STR']
    )


def get_gcp_credentials():
    return Credentials.from_service_account_info(
        get_gcp_service_account_json()
    )


def get_gcs_client():
    return storage.Client(
        project=get_gcp_project(),
        credentials=get_gcp_credentials(),
    )


EXTERNAL_BUCKET_STATEMENTS = [
    {
        'Action': 's3:GetObject',
        'Resource': lambda s: 'arn:aws:s3:::%s/*' % s,
        'Effect': 'Allow',
    },
    {
        'Action': 's3:GetObjectAcl',
        'Resource': lambda s: 'arn:aws:s3:::%s/*' % s,
        'Effect': 'Allow',
    },
]

_FEDERATION_TOKEN_DURATION_SECONDS = 36 * 60 * 60


def _compile_statements_from_list(buckets_list):
    statements = []
    if buckets_list:
        for ext_policy in EXTERNAL_BUCKET_STATEMENTS:
            new_policy = copy.copy(ext_policy)
            new_policy['Resource'] = []
            for line in buckets_list:
                line = line.strip()
                if line:
                    line = line.strip()
                    new_policy['Resource'].append(ext_policy['Resource'](line))
            statements.append(new_policy)
    return statements


def _save_policy_json(policy_json, file_path):
    with open(file_path + '.json', 'w') as file_handler:
        json.dump(policy_json, file_handler)


def _build_external_bucket_json(file_path):
    try:
        with open(file_path) as file_handler:
            policy_json = {
                'Version': '2012-10-17',
                'Statement': [],
            }
            buckets_list = [item.strip() for item in file_handler.readlines()]
            statements = _compile_statements_from_list(buckets_list)
            if statements:
                policy_json['Statement'] = statements
                _save_policy_json(policy_json, file_path)
    except FileNotFoundError:  # pylint: disable=undefined-variable
        print('Could not load external bucket policy list.')


def _get_external_bucket_policy(file_path):
    '''
    Returns a compiled json of external s3 access policies for federated users
    '''
    try:
        with open(file_path + '.json', 'r') as file_handler:
            return json.loads(file_handler.read())
    except FileNotFoundError:  # pylint: disable=undefined-variable
        return None


class S3UploadCredentials(object):
    # pylint: disable=too-few-public-methods
    '''
    Build and distribute federate aws credentials for submitting files
    '''

    def __init__(self, bucket, key, name, sts_client):
        self._bucket = bucket
        self._key = key
        self._name = name
        self._sts_client = sts_client
        file_url = '{bucket}/{key}'.format(
            bucket=self._bucket,
            key=self._key
        )
        self._resource_string = 'arn:aws:s3:::{}'.format(file_url)
        self._upload_url = 's3://{}'.format(file_url)
        self._external_policy = {}

    def _get_base_policy(self):
        policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Action': 's3:PutObject',
                    'Resource': self._resource_string,
                }
            ]
        }
        return policy

    def _get_policy(self):
        policy = self._get_base_policy()
        if (
                self._external_policy and
                self._external_policy.get('Statement') and
                isinstance(self._external_policy['Statement'], list)
        ):
            for statement in self._external_policy['Statement']:
                policy['Statement'].append(statement)
        return policy

    def _get_token(self, policy):
        try:
            token = self._sts_client.get_federation_token(
                Name=self._name,
                Policy=json.dumps(policy),
                DurationSeconds=_FEDERATION_TOKEN_DURATION_SECONDS,
            )
            return token
        except botocore.exceptions.ClientError as ecp:
            print('Warning: ', ecp)
            return None

    def _check_external_policy(self, s3_transfer_allow, s3_transfer_buckets):
        if s3_transfer_allow and s3_transfer_buckets:
            external_policy = _get_external_bucket_policy(s3_transfer_buckets)
            if not isinstance(external_policy, dict):
                _build_external_bucket_json(s3_transfer_buckets)
                external_policy = _get_external_bucket_policy(s3_transfer_buckets)
            if external_policy:
                self._external_policy = external_policy

    def external_creds(self, s3_transfer_allow=False, s3_transfer_buckets=None):
        '''
        Used to get the federate user credentials
        If external s3 buckets exist they will be added to the policy.
        '''
        self._check_external_policy(s3_transfer_allow, s3_transfer_buckets)
        policy = self._get_policy()
        token = self._get_token(policy)
        credentials = {
            'session_token': token.get('Credentials', {}).get('SessionToken'),
            'access_key': token.get('Credentials', {}).get('AccessKeyId'),
            'expiration': token.get('Credentials', {}).get('Expiration').isoformat(),
            'secret_key': token.get('Credentials', {}).get('SecretAccessKey'),
            'upload_url': self._upload_url,
            'federated_user_arn': token.get('FederatedUser', {}).get('Arn'),
            'federated_user_id': token.get('FederatedUser', {}).get('FederatedUserId'),
            'request_id': token.get('ResponseMetadata', {}).get('RequestId')
        }
        return {
            'service': 's3',
            'bucket': self._bucket,
            'key': self._key,
            'upload_credentials': credentials,
        }


class GcsUploadCredentials(object):
    # pylint: disable=too-few-public-methods
    '''
    Build and distribute presigned URLs (https://) for submitting files
    '''

    def __init__(self, bucket, key, name, gcs_client, gcp_credentials):
        self._bucket = bucket
        self._key = key
        self._name = name
        self._gcs_client = gcs_client
        self._file_url = 'gs://{bucket}/{key}'.format(
            bucket=self._bucket,
            key=self._key
        )
        self._gcp_credentials = gcp_credentials

    def _get_presigned_url(self, file_url, expiration_sec):
        '''
        Used to generate a presigned URL for PUT method.
        '''
        try:
            bucket_obj = self._gcs_client.get_bucket(self._bucket)
            blob = storage.Blob(name=self._key, bucket=bucket_obj)

            return blob.generate_signed_url(
                version='V4',
                method='PUT',
                expiration=timedelta(seconds=self._expiration_sec),
                credentials=self._gcp_credentials,
            )

        except ClientError as ecp:
            print('Warning: ', ecp)
            return None

    def external_creds(self):
        '''
        Used to get the presigned URL.
        '''
        expiration_sec = os.environ['GCS_UPLOAD_EXPIRATION_SEC']

        upload_url = self._get_presigned_url(
            file_url=self._file_url,
            expiration_sec=expiration_sec,
        )

        expiration = (
            datetime.now(timezone.utc) + timedelta(seconds=expiration_sec)
        ).isoformat()

        credentials = {
            'expiration': expiration,
            'upload_url': upload_url,
        }
        return {
            'service': 'gcs',
            'bucket': self._bucket,
            'key': self._key,
            'upload_credentials': credentials,
        }
