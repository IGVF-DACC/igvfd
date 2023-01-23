import pytest

from moto import mock_rds


@pytest.fixture(scope='function')
def aws_credentials():
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-1'


def raw_results():
    import datetime
    from dateutil.tz import tzutc
    return [
        {
            'DBSnapshotIdentifier': 'rds:xyz123-demo-rds-2022-05-18-07-14',
            'DBInstanceIdentifier': 'xyz123-demo-rds',
            'SnapshotCreateTime': datetime.datetime(2022, 5, 18, 7, 14, 31, 987000, tzinfo=tzutc()),
            'Engine': 'postgres',
            'AllocatedStorage': 20,
            'Status': 'available',
            'Port': 5432,
            'AvailabilityZone': 'us-west-2a',
            'VpcId': 'vpc-ea3b6581',
            'InstanceCreateTime': datetime.datetime(2021, 11, 23, 0, 30, 2, 358000, tzinfo=tzutc()),
            'MasterUsername': 'postgres',
            'EngineVersion': '14.1',
            'LicenseModel': 'postgresql-license',
            'SnapshotType': 'automated',
            'OptionGroupName': 'default:postgres-14',
            'PercentProgress': 100,
            'StorageType': 'gp2',
            'Encrypted': True,
            'KmsKeyId': 'arn:aws:kms:us-west-2:618537831167:key/8a306d81-4532-4092-ab69-0a5e3ea0e0dd',
            'DBSnapshotArn': 'arn:aws:rds:us-west-2:618537831167:snapshot:rds:xyz123-demo-rds-2022-05-18-07-14',
            'IAMDatabaseAuthenticationEnabled': True,
            'ProcessorFeatures': [],
            'DbiResourceId': 'db-IUNEOMVXF6RR46FOSFSJHGAPNU',
            'TagList': [],
            'OriginalSnapshotCreateTime': datetime.datetime(2022, 5, 18, 7, 14, 31, 987000, tzinfo=tzutc()),
            'SnapshotTarget': 'region'
        },
        {
            'DBSnapshotIdentifier': 'rds:xyz123-demo-rds-2022-05-22-07-13',
            'DBInstanceIdentifier': 'xyz123-demo-rds',
            'SnapshotCreateTime': datetime.datetime(2022, 5, 22, 7, 13, 31, 987000, tzinfo=tzutc()),
            'Engine': 'postgres',
            'AllocatedStorage': 20,
            'Status': 'available',
            'Port': 5432,
            'AvailabilityZone': 'us-west-2a',
            'VpcId': 'vpc-ea3b6581',
            'InstanceCreateTime': datetime.datetime(2021, 11, 23, 0, 30, 2, 358000, tzinfo=tzutc()),
            'MasterUsername': 'postgres',
            'EngineVersion': '14.1',
            'LicenseModel': 'postgresql-license',
            'SnapshotType': 'automated',
            'OptionGroupName': 'default:postgres-14',
            'PercentProgress': 100,
            'StorageType': 'gp2',
            'Encrypted': True,
            'KmsKeyId': 'arn:aws:kms:us-west-2:618537831167:key/8a306d81-4532-4092-ab69-0a5e3ea0e0dd',
            'DBSnapshotArn': 'arn:aws:rds:us-west-2:618537831167:snapshot:rds:xyz123-demo-rds-2022-05-22-07-13',
            'IAMDatabaseAuthenticationEnabled': True,
            'ProcessorFeatures': [],
            'DbiResourceId': 'db-IUNEOMVXF6RR46FOSFSJHGAPNU',
            'TagList': [],
            'OriginalSnapshotCreateTime': datetime.datetime(2022, 5, 22, 7, 14, 31, 987000, tzinfo=tzutc()),
            'SnapshotTarget': 'region'
        },
        {
            'DBSnapshotIdentifier': 'rds:xyz123-demo-rds-2022-05-09-07-13',
            'DBInstanceIdentifier': 'xyz123-demo-rds',
            'SnapshotCreateTime': datetime.datetime(2022, 5, 9, 7, 13, 31, 987000, tzinfo=tzutc()),
            'Engine': 'postgres',
            'AllocatedStorage': 20,
            'Status': 'available',
            'Port': 5432,
            'AvailabilityZone': 'us-west-2a',
            'VpcId': 'vpc-ea3b6581',
            'InstanceCreateTime': datetime.datetime(2021, 11, 23, 0, 30, 2, 358000, tzinfo=tzutc()),
            'MasterUsername': 'postgres',
            'EngineVersion': '14.1',
            'LicenseModel': 'postgresql-license',
            'SnapshotType': 'automated',
            'OptionGroupName': 'default:postgres-14',
            'PercentProgress': 100,
            'StorageType': 'gp2',
            'Encrypted': True,
            'KmsKeyId': 'arn:aws:kms:us-west-2:618537831167:key/8a306d81-4532-4092-ab69-0a5e3ea0e0dd',
            'DBSnapshotArn': 'arn:aws:rds:us-west-2:618537831167:snapshot:rds:xyz123-demo-rds-2022-05-19-07-13',
            'IAMDatabaseAuthenticationEnabled': True,
            'ProcessorFeatures': [],
            'DbiResourceId': 'db-IUNEOMVXF6RR46FOSFSJHGAPNU',
            'TagList': [],
            'OriginalSnapshotCreateTime': datetime.datetime(2022, 5, 9, 7, 14, 31, 987000, tzinfo=tzutc()),
            'SnapshotTarget': 'region'
        },
    ]


@mock_rds
def test_runtime_lambdas_rds_snapshot_get_rds_client(aws_credentials):
    from snapshot.main import get_rds_client
    client = get_rds_client()
    assert hasattr(client, 'describe_db_snapshots')


@mock_rds
def test_runtime_lambdas_rds_snapshot_get_paginator(aws_credentials):
    from snapshot.main import get_rds_client
    from snapshot.main import get_describe_db_snapshots_paginator
    from botocore.paginate import Paginator
    client = get_rds_client()
    paginator = get_describe_db_snapshots_paginator(client)
    assert isinstance(paginator, Paginator)


@mock_rds
def test_runtime_lambdas_rds_snapshot_make_query(aws_credentials):
    from snapshot.main import get_rds_client
    from snapshot.main import get_describe_db_snapshots_paginator
    from snapshot.main import make_query
    client = get_rds_client()
    paginator = get_describe_db_snapshots_paginator(client)
    query = make_query(paginator, some_key='some_value')
    assert query._op_kwargs == {'some_key': 'some_value'}


@mock_rds
def test_runtime_lambdas_rds_snapshot_get_results(aws_credentials):
    from snapshot.main import get_rds_client
    from snapshot.main import get_describe_db_snapshots_paginator
    from snapshot.main import make_query
    from snapshot.main import get_results
    client = get_rds_client()
    paginator = get_describe_db_snapshots_paginator(client)
    query = make_query(paginator, DBInstanceIdentifier='some_value')
    results = list(get_results(query))
    assert results == []


@mock_rds
def test_runtime_lambdas_rds_snapshot_sort_results_by_create_time(aws_credentials):
    from snapshot.main import sort_results_by_create_time
    sorted_results = sort_results_by_create_time(raw_results())
    assert (
        sorted_results[0]['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'
    )


@mock_rds
def test_runtime_lambdas_rds_snapshot_get_latest_result(aws_credentials):
    from snapshot.main import sort_results_by_create_time
    from snapshot.main import get_latest_result
    sorted_results = sort_results_by_create_time(raw_results())
    latest_result = get_latest_result(sorted_results)
    assert latest_result['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'


@mock_rds
def test_runtime_lambdas_rds_snapshot_get_latest_snapshot_id(aws_credentials, mocker):
    from snapshot.main import get_latest_rds_snapshot_id
    mocker.patch(
        'snapshot.main.get_results',
        return_value=raw_results()
    )
    latest_snapshot = get_latest_rds_snapshot_id(
        event={
            'ResourceProperties': {
                'db_instance_identifier': 'xyz123-demo-rds',
            }
        },
        context={}
    )
    assert latest_snapshot['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'
    assert (
        latest_snapshot['DBSnapshotArn'] == 'arn:aws:rds:us-west-2:618537831167:snapshot:rds:xyz123-demo-rds-2022-05-22-07-13'
    )


@mock_rds
def test_runtime_lambdas_rds_snapshot_on_create(aws_credentials, mocker):
    from snapshot.main import on_create
    mocker.patch(
        'snapshot.main.get_results',
        return_value=raw_results()
    )
    results = on_create(
        event={
            'ResourceProperties': {
                'db_instance_identifier': 'xyz123-demo-rds',
            }
        },
        context={}
    )
    assert results['Data']['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'


@mock_rds
def test_runtime_lambdas_rds_snapshot_custom_resource_handler(aws_credentials, mocker):
    from snapshot.main import custom_resource_handler
    mocker.patch(
        'snapshot.main.get_results',
        return_value=raw_results()
    )
    event = {
        'ResourceProperties': {
            'db_instance_identifier': 'xyz123-demo-rds',
        }
    }
    event['RequestType'] = 'Create'
    response = custom_resource_handler(
        event=event,
        context={}
    )
    assert response['Data']['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'
    event['RequestType'] = 'Update'
    response = custom_resource_handler(
        event=event,
        context={}
    )
    assert response['Data']['DBSnapshotIdentifier'] == 'rds:xyz123-demo-rds-2022-05-22-07-13'
    event['RequestType'] = 'Delete'
    response = custom_resource_handler(
        event=event,
        context={}
    )
    assert response is None
