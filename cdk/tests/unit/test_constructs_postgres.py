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


@pytest.mark.skip()
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
            instance_type=instance_type
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


@pytest.mark.skip()
def test_constructs_postgres_initialize_postgres_from_snapshot_construct(stack, vpc, instance_type, mocker):
    from infrastructure.constructs.postgres import PostgresFromSnapshot
    from infrastructure.constructs.postgres import PostgresProps
    from infrastructure.config import Config
    config = Config(
        name='demo',
        branch='some-branch',
        pipeline='DemoPipeline',
        snapshot_source_db_identifier='source-db-123'
    )
    # Given
    existing_resources = mocker.Mock()
    existing_resources.network.vpc = vpc
    # When
    postgres = PostgresFromSnapshot(
        stack,
        'PostgresFromSnapshot',
        props=PostgresProps(
            config=config,
            existing_resources=existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=instance_type
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
            'PolicyName': 'PostgresFromSnapshotLatestSnapshotFromDBGetLatestRDSSnapshotIDServiceRoleDefaultPolicy98F8C942',
            'Roles': [
                {
                    'Ref': 'PostgresFromSnapshotLatestSnapshotFromDBGetLatestRDSSnapshotIDServiceRole00AE3DDA'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::CloudFormation::CustomResource',
        {
            'ServiceToken': {
                'Fn::GetAtt': [
                    'PostgresFromSnapshotLatestSnapshotFromDBProviderframeworkonEvent8F67E899',
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
                    'Key': 'from_snapshot_arn',
                    'Value': {
                        'Fn::GetAtt': [
                            'PostgresFromSnapshotLatestSnapshotFromDBLatestRDSSnapshopIDCA971DA9',
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


def test_constructs_postgres_postgres_factory():
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresFromSnapshot
    from infrastructure.constructs.postgres import postgres_factory
    from infrastructure.config import Config
    config = Config(
        name='demo',
        branch='xyz',
        pipeline='zyx',
    )
    postgres = postgres_factory(config)
    assert issubclass(postgres, Postgres)
    config = Config(
        name='demo',
        branch='xyz',
        pipeline='zyx',
        snapshot_source_db_identifier='source-db-id',
    )
    postgres = postgres_factory(config)
    assert issubclass(postgres, PostgresFromSnapshot)
