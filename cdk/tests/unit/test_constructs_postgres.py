import pytest

from aws_cdk.assertions import Template
from aws_cdk.assertions import Match


def test_constructs_postgres_initialize_postgres_construct(stack, vpc, instance_type, mocker):
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresProps
    from infrastructure.config import Config
    # Given
    existing_resources = mocker.Mock()
    existing_resources.network.vpc = vpc
    # When
    postgres = Postgres(
        stack,
        'Postgres',
        props=PostgresProps(
            config=Config(
                branch='my-branch',
                pipeline='xyz',
            ),
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
                {'Key': 'branch', 'Value': 'my-branch'}
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
                    'Value': 'my-branch'
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
                    'Value': 'my-branch'
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
