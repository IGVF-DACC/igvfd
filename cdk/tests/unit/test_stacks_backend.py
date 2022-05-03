import pytest

from aws_cdk.assertions import Template


def test_stacks_backend_initialize_backend_stack():
    from aws_cdk import App
    from infrastructure.stacks.postgres import PostgresStack
    from infrastructure.stacks.backend import BackendStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    branch = 'some-branch'
    postgres_stack = PostgresStack(
        app,
        'TestPostgresStack',
        branch=branch,
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )
    backend_stack = BackendStack(
        app,
        'TestBackendStack',
        branch=branch,
        postgres=postgres_stack.postgres,
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
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
