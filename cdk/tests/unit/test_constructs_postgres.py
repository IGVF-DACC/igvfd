import pytest

from aws_cdk.assertions import Template
from aws_cdk.assertions import Match


def test_constructs_postgres_initialize_postgres_base_construct(stack, config, instance_type, mocker, existing_resources, postgres_engine_version):
    from infrastructure.constructs.postgres import PostgresBase
    from infrastructure.constructs.postgres import PostgresProps
    from jsii._reference_map import _refs
    from aws_cdk.aws_rds import IInstanceEngine
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type,
        engine_version=postgres_engine_version,
    )
    postgres_base = PostgresBase(
        stack,
        'PostgresBase',
        props=props,
    )
    assert postgres_base.engine is not None
    assert postgres_base.database_name == 'igvfd'


def test_constructs_postgres_initialize_postgres_construct(stack, vpc, instance_type, mocker, config, existing_resources, postgres_engine_version):
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresProps
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
            engine_version=postgres_engine_version,
        )
    )
    # Then
    template = Template.from_stack(stack)
    assert len(template.to_json()['Outputs']) == 3
    template.has_output(
        'ExportsOutputFnGetAttPostgres97B73533EndpointAddress94521E53',
        {
            'Value': {
                'Fn::GetAtt': [
                    'Postgres97B73533', 'Endpoint.Address']
            },
            'Export': {
                'Name': 'Default:ExportsOutputFnGetAttPostgres97B73533EndpointAddress94521E53'
            }
        }
    )
    template.has_output(
        'ExportsOutputRefPostgresSecretAttachment5D653F4FA8D767F0',
        {
            'Value': {
                'Ref': 'PostgresSecretAttachment5D653F4F'
            },
            'Export': {
                'Name': 'Default:ExportsOutputRefPostgresSecretAttachment5D653F4FA8D767F0'
            }
        }
    )
    template.has_output(
        'ExportsOutputFnGetAttPostgresSecurityGroupA2E13118GroupId7C742499',
        {
            'Value': {
                'Fn::GetAtt': ['PostgresSecurityGroupA2E13118', 'GroupId']},
            'Export': {
                'Name': 'Default:ExportsOutputFnGetAttPostgresSecurityGroupA2E13118GroupId7C742499'
            }
        }
    )
    expected = {
        'Type': 'AWS::RDS::DBInstance',
        'Properties': {
            'DBInstanceClass': 'db.t3.medium',
            'AllocatedStorage': '10',
            'AutoMinorVersionUpgrade': False,
            'CopyTagsToSnapshot': True,
            'DBName': 'igvfd',
            'DBSubnetGroupName': {'Ref': 'PostgresSubnetGroup68192ADF'},
            'EnablePerformanceInsights': True,
            'Engine': 'postgres',
            'EngineVersion': '14.3',
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
            'PerformanceInsightsRetentionPeriod': 7,
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
        2
    )


def test_constructs_postgres_initialize_postgres_from_snapshot_arn_construct(stack, vpc, instance_type, mocker, config, existing_resources, postgres_engine_version):
    from infrastructure.constructs.postgres import PostgresFromSnapshotArn
    from infrastructure.constructs.postgres import PostgresProps
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
            engine_version=postgres_engine_version,
            snapshot_arn='some-arn-xyz',
        )
    )
    # Then
    template = Template.from_stack(stack)
    assert len(template.to_json()['Outputs']) == 3
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


def test_constructs_postgres_initialize_postgres_from_latest_snapshot_construct(stack, vpc, instance_type, mocker, config, existing_resources, postgres_engine_version):
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
            engine_version=postgres_engine_version,
            snapshot_source_db_identifier='source-db-123'
        )
    )
    # Then
    template = Template.from_stack(stack)
    assert len(template.to_json()['Outputs']) == 4
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


def test_constructs_postgres_postgres_factory(config, existing_resources, instance_type, postgres_engine_version):
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
        instance_type=instance_type,
        engine_version=postgres_engine_version,
    )
    postgres = postgres_factory(props)
    assert issubclass(postgres, Postgres)
    props = PostgresProps(
        config=config,
        existing_resources=existing_resources,
        allocated_storage=10,
        max_allocated_storage=20,
        instance_type=instance_type,
        engine_version=postgres_engine_version,
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
        engine_version=postgres_engine_version,
        snapshot_source_db_identifier='source-db-id',
    )
    postgres = postgres_factory(props)
    assert issubclass(postgres, PostgresFromLatestSnapshot)
