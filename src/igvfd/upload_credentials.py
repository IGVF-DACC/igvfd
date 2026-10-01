import json
import os

import boto3
import botocore

from botocore.client import BaseClient

from typing import Optional


_FEDERATION_TOKEN_DURATION_SECONDS = 18 * 60 * 60


EXTERNAL_BUCKETS_BY_LAB_UUID = {
    #    'cfb789b8-46f3-4d59-a2b3-adc39e7df93a': [
    #        'test-upload',
    #        'test-upload2',
    #    ],
}


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


def get_restricted_upload_files_user_access_key_and_secret_access_key():
    client = get_secretsmanager_client()
    return json.loads(
        client.get_secret_value(
            SecretId=os.environ['RESTRICTED_UPLOAD_USER_ACCESS_KEYS_SECRET_ARN']
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


def get_restricted_sts_client(localstack_endpoint_url: Optional[str] = None) -> BaseClient:
    if localstack_endpoint_url is not None:
        return boto3.client(
            'sts',
            endpoint_url=localstack_endpoint_url,
            aws_access_key_id='testing',
            aws_secret_access_key='testing',
            region_name='us-west-2',
        )
    restricted_upload_files_user_keys = get_restricted_upload_files_user_access_key_and_secret_access_key()
    return boto3.client(
        'sts',
        aws_access_key_id=restricted_upload_files_user_keys['ACCESS_KEY'],
        aws_secret_access_key=restricted_upload_files_user_keys['SECRET_ACCESS_KEY'],
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


def get_statements_for_external_bucket(bucket):
    return [
        {
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket}/*',
            'Effect': 'Allow',
        },
    ]


class UploadCredentials(object):
    # pylint: disable=too-few-public-methods
    '''
    Build and distribute federate aws credentials for submitting files
    '''

    def __init__(
            self,
            bucket,
            key,
            name,
            sts_client,
            external_buckets_by_lab_uuid=EXTERNAL_BUCKETS_BY_LAB_UUID
    ):
        self._bucket = bucket
        self._key = key
        self._name = name
        self._sts_client = sts_client
        self._external_buckets_by_lab_uuid = external_buckets_by_lab_uuid
        file_url = '{bucket}/{key}'.format(
            bucket=self._bucket,
            key=self._key
        )
        self._resource_string = 'arn:aws:s3:::{}'.format(file_url)
        self._upload_url = 's3://{}'.format(file_url)
        self._external_bucket_statements = []

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
        for statement in self._external_bucket_statements:
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

    def _generate_external_bucket_statements(self, buckets):
        for bucket in buckets:
            self._external_bucket_statements.extend(
                get_statements_for_external_bucket(
                    bucket
                )
            )

    def external_creds(self, lab_uuid=None):
        '''
        Used to get the federate user credentials
        If a lab with external s3 buckets exist they will be added to the policy.
        '''
        if lab_uuid and lab_uuid in self._external_buckets_by_lab_uuid:
            buckets = self._external_buckets_by_lab_uuid[lab_uuid]
            self._generate_external_bucket_statements(buckets)
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
