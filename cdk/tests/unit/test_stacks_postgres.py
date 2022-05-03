import pytest


from aws_cdk.assertions import Template


def test_stacks_postgres_initialize_postgres_stack():
    from aws_cdk import App
    from infrastructure.stacks.postgres import PostgresStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    postgres_stack = PostgresStack(
        app,
        'TestPostgresStack',
        branch='some-branch',
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )
    template = Template.from_stack(postgres_stack)
    template.has_resource_properties(
        'AWS::RDS::DBInstance',
        {
            'DBInstanceClass': 'db.t3.medium',
            'AllocatedStorage': '10',
            'CopyTagsToSnapshot': True,
            'DBName': 'igvfd',
            'DBSubnetGroupName': {
                'Ref': 'PostgresSubnetGroup68192ADF'
            },
            'Engine': 'postgres',
            'EngineVersion': '14.1',
            'MasterUsername': {
                'Fn::Join': [
                    '',
                    [
                        '{{resolve:secretsmanager:',
                        {
                            'Ref': 'PostgresSecret2F50519E'
                        },
                        ':SecretString:username::}}'
                    ]
                ]
            },
            'MasterUserPassword': {
                'Fn::Join': [
                    '',
                    [
                        '{{resolve:secretsmanager:',
                        {
                            'Ref': 'PostgresSecret2F50519E'
                        },
                        ':SecretString:password::}}'
                    ]
                ]
            },
            'MaxAllocatedStorage': 20,
            'PubliclyAccessible': False,
            'StorageType': 'gp2',
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'VPCSecurityGroups': [
                {
                    'Fn::GetAtt': [
                        'PostgresSecurityGroupA2E13118',
                        'GroupId'
                    ]
                }
            ]
        }
    )
