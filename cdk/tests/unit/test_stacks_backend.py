import pytest

from aws_cdk.assertions import Template


def test_stacks_backend_initialize_backend_stack(config):
    from aws_cdk import App
    from infrastructure.stacks.postgres import PostgresStack
    from infrastructure.stacks.backend import BackendStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    postgres_stack = PostgresStack(
        app,
        'TestPostgresStack',
        existing_resources_class=igvf_dev.Resources,
        config=config,
        env=igvf_dev.US_WEST_2,
    )
    backend_stack = BackendStack(
        app,
        'TestBackendStack',
        config=config,
        postgres_multiplexer=postgres_stack.multiplexer,
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )
    template = Template.from_stack(postgres_stack)
    assert len(template.to_json()['Outputs']) == 3
    template.has_output(
        'ExportsOutputFnGetAttPostgres97B73533EndpointAddress94521E53',
        {
            'Value': {
                'Fn::GetAtt': [
                    'Postgres97B73533',
                    'Endpoint.Address'
                ]
            },
            'Export': {
                'Name': 'TestPostgresStack:ExportsOutputFnGetAttPostgres97B73533EndpointAddress94521E53'
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
                'Name': 'TestPostgresStack:ExportsOutputRefPostgresSecretAttachment5D653F4FA8D767F0'
            }
        }
    )
    template.has_output(
        'ExportsOutputFnGetAttPostgresSecurityGroupA2E13118GroupId7C742499',
        {
            'Value': {
                'Fn::GetAtt': [
                    'PostgresSecurityGroupA2E13118',
                    'GroupId'
                ]
            },
            'Export': {
                'Name': 'TestPostgresStack:ExportsOutputFnGetAttPostgresSecurityGroupA2E13118GroupId7C742499'
            }
        }
    )
    template = Template.from_stack(backend_stack)
    template.has_resource_properties(
        'AWS::ECS::Service',
        {
            'Cluster': {
                'Ref': 'EcsDefaultClusterMnL3mNNYNDemoVpc278C9613'
            },
            'DeploymentConfiguration': {
                'DeploymentCircuitBreaker': {
                    'Enable': True,
                    'Rollback': True
                },
                'MaximumPercent': 200,
                'MinimumHealthyPercent': 50
            },
            'DeploymentController': {
                'Type': 'ECS'
            },
            'DesiredCount': 1,
            'EnableECSManagedTags': False,
            'EnableExecuteCommand': True,
            'HealthCheckGracePeriodSeconds': 60,
            'LaunchType': 'FARGATE',
            'LoadBalancers': [
                {
                    'ContainerName': 'nginx',
                    'ContainerPort': 80,
                    'TargetGroupArn': {
                        'Ref': 'BackendFargateLBPublicListenerECSGroupD246B499'
                    }
                }
            ],
            'NetworkConfiguration': {
                'AwsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',
                    'SecurityGroups': [
                        {
                            'Fn::GetAtt': [
                                'BackendFargateServiceSecurityGroupC1AC366B',
                                'GroupId'
                            ]
                        }
                    ],
                    'Subnets': [
                        's-12345',
                        's-67890'
                    ]
                }
            },
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'TaskDefinition': {
                'Ref': 'BackendFargateTaskDef2A6FD509'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'Description': 'Allow connection to Postgres instance',
            'FromPort': 5432,
            'GroupId': {
                'Fn::ImportValue': 'TestPostgresStack:ExportsOutputFnGetAttPostgresSecurityGroupA2E13118GroupId7C742499'
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    'BackendFargateServiceSecurityGroupC1AC366B',
                    'GroupId'
                ]
            },
            'ToPort': 5432
        }
    )
