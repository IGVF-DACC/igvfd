import json
import os
import boto3

from botocore.client import BaseClient

from igvfd.upload_credentials import get_secretsmanager_client

from typing import Optional


CHECKFILES_SECRET_ARN = 'arn:aws:secretsmanager:us-west-2:109189702753:secret:checkfiles-user-igvf-buckets-read-key-nYYKOz'
FEDERATION_TOKEN_DURATION_SECONDS = 3600*24


def get_bucket_mount_policy():
    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': [
                    's3:GetBucketAcl',
                    's3:GetBucketLocation',
                    's3:GetObject',
                    's3:GetObjectVersion',
                    's3:ListBucket'
                ],
                'Resource': [
                    'arn:aws:s3:::checkfiles-test',
                    'arn:aws:s3:::checkfiles-test/*'
                ]
            }
        ]
    }
    return policy


def get_secret_from_arn(arn: str) -> dict:
    client = get_secretsmanager_client()
    return json.loads(
        client.get_secret_value(
            SecretId=arn
        )['SecretString']
    )


def get_checkfiles_user_keys():
    return get_secret_from_arn(CHECKFILES_SECRET_ARN)


def get_sts_client(localstack_endpoint_url: Optional[str] = None) -> BaseClient:
    if localstack_endpoint_url is not None:
        return boto3.client(
            'sts',
            endpoint_url=localstack_endpoint_url,
            aws_access_key_id='testing',
            aws_secret_access_key='testing',
            region_name='us-west-2',
        )
    checkfiles_user_keys = get_checkfiles_user_keys()
    return boto3.client(
        'sts',
        aws_access_key_id=checkfiles_user_keys['ACCESS_KEY'],
        aws_secret_access_key=checkfiles_user_keys['SECRET_ACCESS_KEY'],
        region_name='us-west-2',
    )


def get_checkfiles_mount_token():
    policy = get_bucket_mount_policy()
    client = get_sts_client()
    token = client.get_federation_token(
        Name='checkfiles_token',
        Policy=json.dumps(policy),
        DurationSeconds=FEDERATION_TOKEN_DURATION_SECONDS,
    )
    return token


def get_checkfiles_mount_credentials():
    token = get_checkfiles_mount_token()
    credentials = {
        'session_token': token.get('Credentials', {}).get('SessionToken'),
        'access_key': token.get('Credentials', {}).get('AccessKeyId'),
        'expiration': token.get('Credentials', {}).get('Expiration').isoformat(),
        'secret_key': token.get('Credentials', {}).get('SecretAccessKey'),
        'federated_user_arn': token.get('FederatedUser', {}).get('Arn'),
        'federated_user_id': token.get('FederatedUser', {}).get('FederatedUserId'),
        'request_id': token.get('ResponseMetadata', {}).get('RequestId')
    }
