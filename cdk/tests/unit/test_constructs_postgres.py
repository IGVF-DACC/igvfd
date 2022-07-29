import pytest

from aws_cdk.assertions import Template
from aws_cdk.assertions import Match


def test_constructs_postgres_initialize_postgres_base_construct(stack, config, instance_type, mocker):
    from infrastructure.constructs.postgres import PostgresBase
    from infrastructure.constructs.postgres import PostgresProps
    from jsii._reference_map import _refs
    from aws_cdk.aws_rds import IInstanceEngine
    existing_resources = mocker.Mock()
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type
    )
    postgres_base = PostgresBase(
        stack,
        'PostgresBase',
        props=props,
    )
    assert postgres_base.engine is not None
    assert postgres_base.database_name == 'igvfd'


def test_constructs_postgres_initialize_postgres_construct(stack, vpc, instance_type, mocker, config):
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresProps
    # Given
    existing_resources = mocker.Mock()
    existing_resources.network.vpc = vpc
    # When
    postgres = Postgres(
        stack,
        'Postgres',
        props=PostgresProps(
            config=config,
            existing_resources=existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=instance_type,
        )
    )
    # Then
    template = Template.from_stack(stack)
    expected = {
        'Type': 'AWS::RDS::DBInstance',
        'Properties': {
            'DBInstanceClass': 'db.t3.medium',
            'AllocatedStorage': '10',
            'CopyTagsToSnapshot': True,
            'DBName': 'igvfd',
            'DBSubnetGroupName': {'Ref': 'PostgresSubnetGroup68192ADF'},
            'Engine': 'postgres',
            'EngineVersion': '14.1',
            'MasterUsername': {
                'Fn::Join': [
                    '',
                    [
                        '{{resolve:secretsmanager:',
                        {'Ref': 'PostgresSecret2F50519E'},
                        ':SecretString:username::}}'
                    ]
                ]
            },
            'MasterUserPassword': {
                'Fn::Join': [
                    '',
                    [
                        '{{resolve:secretsmanager:',
                        {'Ref': 'PostgresSecret2F50519E'},
                        ':SecretString:password::}}'
                    ]
                ]
            },
            'MaxAllocatedStorage': 20,
            'PubliclyAccessible': False,
            'StorageType': 'gp2',
            'Tags': [
                {'Key': 'branch', 'Value': 'some-branch'}
            ],
            'VPCSecurityGroups': [
                {
                    'Fn::GetAtt': [
                        'PostgresSecurityGroupA2E13118',
                        'GroupId'
                    ]
                }
            ]
        },
        'UpdateReplacePolicy': 'Snapshot',
        'DeletionPolicy': 'Snapshot'
    }
    template.has_resource(
        'AWS::RDS::DBInstance',
        Match.object_equals(expected)
    )
    template.resource_count_is(
        'AWS::RDS::DBInstance',
        1
    )
    template.has_resource_properties(
        'AWS::RDS::DBSubnetGroup',
        {
            'DBSubnetGroupDescription': 'Subnet group for Postgres database',
            'SubnetIds': [
                {
                    'Ref': 'TestVpcisolatedSubnet1Subnet2860A680'
                },
                {
                    'Ref': 'TestVpcisolatedSubnet2SubnetA6454F0B'
                }
            ],
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroup',
        {
            'GroupDescription': 'Security group for Postgres database',
            'SecurityGroupEgress': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow all outbound traffic by default',
                    'IpProtocol': '-1'
                }
            ],
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'VpcId': {
                'Ref': 'TestVpcE77CE678'
            }
        }
    )
    template.resource_count_is(
        'AWS::SecretsManager::Secret',
        1
    )


def test_constructs_postgres_initialize_postgres_from_snapshot_arn_construct(stack, vpc, instance_type, mocker, config):
    from infrastructure.constructs.postgres import PostgresFromSnapshotArn
    from infrastructure.constructs.postgres import PostgresProps
    # Given
    existing_resources = mocker.Mock()
    existing_resources.network.vpc = vpc
    # When
    postgres = PostgresFromSnapshotArn(
        stack,
        'PostgresFromSnapshotArn',
        props=PostgresProps(
            config=config,
            existing_resources=existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=instance_type,
            snapshot_arn='some-arn-xyz',
        )
    )
    # Then
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::CloudFormation::CustomResource',
        0
    )
    template.resource_count_is(
        'AWS::SecretsManager::SecretTargetAttachment',
        1
    )
    template.has_resource_properties(
        'AWS::RDS::DBInstance',
        {
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                },
                {
                    'Key': 'snapshot_arn',
                    'Value': 'some-arn-xyz',
                }
            ],
        }
    )


def test_constructs_postgres_initialize_postgres_from_latest_snapshot_construct(stack, vpc, instance_type, mocker, config, existing_resources):
    from infrastructure.constructs.postgres import PostgresFromLatestSnapshot
    from infrastructure.constructs.postgres import PostgresProps
    # Given
    existing_resources.network.vpc = vpc
    # When
    postgres = PostgresFromLatestSnapshot(
        stack,
        'PostgresFromLatestSnapshot',
        props=PostgresProps(
            config=config,
            existing_resources=existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=instance_type,
            snapshot_source_db_identifier='source-db-123'
        )
    )
    # Then
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': 'rds:DescribeDBSnapshots',
                        'Effect': 'Allow',
                        'Resource': '*'
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'PostgresFromLatestSnapshotLatestSnapshotFromDBGetLatestRDSSnapshotIDServiceRoleDefaultPolicyFCFE06D5',
            'Roles': [
                {
                    'Ref': 'PostgresFromLatestSnapshotLatestSnapshotFromDBGetLatestRDSSnapshotIDServiceRoleC6B5E8E4',
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::CloudFormation::CustomResource',
        {
            'ServiceToken': {
                'Fn::GetAtt': [
                    'PostgresFromLatestSnapshotLatestSnapshotFromDBProviderframeworkonEvent034F8EB7',
                    'Arn'
                ]
            },
            'db_instance_identifier': 'source-db-123'
        }
    )
    template.resource_count_is(
        'AWS::SecretsManager::SecretTargetAttachment',
        1
    )
    template.has_resource_properties(
        'AWS::RDS::DBInstance',
        {
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                },
                {
                    'Key': 'latest_snapshot_arn',
                    'Value': {
                        'Fn::GetAtt': [
                            'PostgresFromLatestSnapshotLatestSnapshotFromDBLatestRDSSnapshotIDC2E57373',
                            'DBSnapshotArn'
                        ]
                    }
                },
                {
                    'Key': 'snapshot_source_db_identifier',
                    'Value': 'source-db-123'
                }
            ],
        }
    )


def test_constructs_postgres_postgres_factory(config, existing_resources, instance_type):
    from infrastructure.constructs.postgres import PostgresProps
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresFromSnapshotArn
    from infrastructure.constructs.postgres import PostgresFromLatestSnapshot
    from infrastructure.constructs.postgres import postgres_factory
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type
    )
    postgres = postgres_factory(props)
    assert issubclass(postgres, Postgres)
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type,
        snapshot_arn='some-arn-xyz',
    )
    postgres = postgres_factory(props)
    assert issubclass(postgres, PostgresFromSnapshotArn)
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type,
        snapshot_source_db_identifier='source-db-id',
    )
    postgres = postgres_factory(props)
    assert issubclass(postgres, PostgresFromLatestSnapshot)
