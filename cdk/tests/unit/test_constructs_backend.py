import pytest

from aws_cdk.assertions import Template


def test_constructs_backend_initialize_backend_construct(stack, instance_type, existing_resources, vpc):
    from infrastructure.constructs.backend import Backend
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresProps
    from infrastructure.config import Config
    # Given
    branch = 'some-branch'
    postgres = Postgres(
        stack,
        'Postgres',
        props=PostgresProps(
            config=Config(
                branch=branch,
                pipeline='xyz',
            ),
            existing_resources=existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=instance_type
        )
    )
    # When
    backend = Backend(
        stack,
        'TestBackend',
        branch=branch,
        postgres=postgres,
        existing_resources=existing_resources,
        cpu=2048,
        memory_limit_mib=4096,
        desired_count=4,
        max_capacity=7,
    )
    template = Template.from_stack(stack)
    # Then
    template.resource_count_is(
        'AWS::ECS::Cluster',
        1
    )
    template.has_resource_properties(
        'AWS::ECS::Service',
        {
            'Cluster': {
                'Ref': 'EcsDefaultClusterMnL3mNNYNTestVpc4872C696'
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
            'DesiredCount': 4,
            'EnableECSManagedTags': False,
            'EnableExecuteCommand': True,
            'HealthCheckGracePeriodSeconds': 60,
            'LaunchType': 'FARGATE',
            'LoadBalancers': [
                {
                    'ContainerName': 'nginx',
                    'ContainerPort': 80,
                    'TargetGroupArn': {
                        'Ref': 'TestBackendFargateLBPublicListenerECSGroupAE2BAFBC'
                    }
                }
            ],
            'NetworkConfiguration': {
                'AwsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',
                    'SecurityGroups': [
                        {
                            'Fn::GetAtt': [
                                'TestBackendFargateServiceSecurityGroupB9C36B85',
                                'GroupId'
                            ]
                        }
                    ],
                    'Subnets': [
                        {
                            'Ref': 'TestVpcpublicSubnet1Subnet4F70BC85'
                        },
                        {
                            'Ref': 'TestVpcpublicSubnet2Subnet96FF72E6'
                        }
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
                'Ref': 'TestBackendFargateTaskDef9FA612FC'
            }
        }
    )
    template.has_resource_properties(
        'AWS::ECS::TaskDefinition',
        {
            'ContainerDefinitions': [
                {
                    'Essential': True,
                    'LogConfiguration': {
                        'LogDriver': 'awslogs',
                        'Options': {
                            'awslogs-group': {
                                'Ref': 'TestBackendFargateTaskDefnginxLogGroupDF848E6A'
                            },
                            'awslogs-stream-prefix': 'nginx',
                            'awslogs-region': {
                                'Ref': 'AWS::Region'
                            },
                            'mode': 'non-blocking'
                        }
                    },
                    'Name': 'nginx',
                    'PortMappings': [
                        {
                            'ContainerPort': 80,
                            'Protocol': 'tcp'
                        }
                    ]
                },
                {
                    'Environment': [
                        {
                            'Name': 'DB_HOST',
                            'Value': {
                                'Fn::GetAtt': [
                                    'Postgres97B73533',
                                    'Endpoint.Address'
                                ]
                            }
                        },
                        {
                            'Name': 'DB_NAME',
                            'Value': 'igvfd'
                        }
                    ],
                    'Essential': True,
                    'LogConfiguration': {
                        'LogDriver': 'awslogs',
                        'Options': {
                            'awslogs-group': {
                                'Ref': 'TestBackendFargateTaskDefApplicationContainerLogGroup789479BA'
                            },
                            'awslogs-stream-prefix': 'pyramid',
                            'awslogs-region': {
                                'Ref': 'AWS::Region'
                            },
                            'mode': 'non-blocking'
                        }
                    },
                    'Name': 'pyramid',
                    'Secrets': [
                        {
                            'Name': 'DB_PASSWORD',
                            'ValueFrom': {
                                'Fn::Join': [
                                    '',
                                    [
                                        {
                                            'Ref': 'PostgresSecretAttachment5D653F4F'
                                        },
                                        ':password::'
                                    ]
                                ]
                            }
                        }
                    ]
                }
            ],
            'Cpu': '2048',
            'ExecutionRoleArn': {
                'Fn::GetAtt': [
                    'TestBackendFargateTaskDefExecutionRoleD2B7AC7A',
                    'Arn'
                ]
            },
            'Family': 'TestBackendFargateTaskDefD5085BAB',
            'Memory': '4096',
            'NetworkMode': 'awsvpc',
            'RequiresCompatibilities': [
                'FARGATE'
            ],
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'TaskRoleArn': {
                'Fn::GetAtt': [
                    'TestBackendFargateTaskDefTaskRoleD1640BC4',
                    'Arn'
                ]
            }
        }
    )
    template.has_resource_properties(
        'AWS::ElasticLoadBalancingV2::LoadBalancer',
        {
            'LoadBalancerAttributes': [
                {
                    'Key': 'deletion_protection.enabled',
                    'Value': 'false'
                }
            ],
            'Scheme': 'internet-facing',
            'SecurityGroups': [
                {
                    'Fn::GetAtt': [
                        'TestBackendFargateLBSecurityGroupB9A1EF40',
                        'GroupId'
                    ]
                }
            ],
            'Subnets': [
                {
                    'Ref': 'TestVpcpublicSubnet1Subnet4F70BC85'
                },
                {
                    'Ref': 'TestVpcpublicSubnet2Subnet96FF72E6'
                }
            ],
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'Type': 'application'
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroup',
        {
            'GroupDescription': 'Automatically created Security Group for ELB TestBackendFargateLB09584891',
            'SecurityGroupIngress': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow from anyone on port 443',
                    'FromPort': 443,
                    'IpProtocol': 'tcp',
                    'ToPort': 443
                },
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow from anyone on port 80',
                    'FromPort': 80,
                    'IpProtocol': 'tcp',
                    'ToPort': 80
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
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupEgress',
        {
            'GroupId': {
                'Fn::GetAtt': [
                    'TestBackendFargateLBSecurityGroupB9A1EF40',
                    'GroupId'
                ]
            },
            'IpProtocol': 'tcp',
            'Description': 'Load balancer to target',
            'DestinationSecurityGroupId': {
                'Fn::GetAtt': [
                    'TestBackendFargateServiceSecurityGroupB9C36B85',
                    'GroupId'
                ]
            },
            'FromPort': 80,
            'ToPort': 80
        }
    )
    template.has_resource_properties(
        'AWS::ElasticLoadBalancingV2::Listener',
        {
            'DefaultActions': [
                {
                    'TargetGroupArn': {
                        'Ref': 'TestBackendFargateLBPublicListenerECSGroupAE2BAFBC'
                    },
                    'Type': 'forward'
                }
            ],
            'LoadBalancerArn': {
                'Ref': 'TestBackendFargateLB8D39193B'
            },
            'Certificates': [
                {
                    'CertificateArn': {
                        'Ref': 'TestCertificate6B4956B6'
                    }
                }
            ],
            'Port': 443,
            'Protocol': 'HTTPS'
        }
    )
    template.has_resource_properties(
        'AWS::ElasticLoadBalancingV2::Listener',
        {
            'DefaultActions': [
                {
                    'RedirectConfig': {
                        'Port': '443',
                        'Protocol': 'HTTPS',
                        'StatusCode': 'HTTP_301'
                    },
                    'Type': 'redirect'
                }
            ],
            'LoadBalancerArn': {
                'Ref': 'TestBackendFargateLB8D39193B'
            },
            'Port': 80,
            'Protocol': 'HTTP'
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': [
                            'ecr:BatchCheckLayerAvailability',
                            'ecr:GetDownloadUrlForLayer',
                            'ecr:BatchGetImage'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::Join': [
                                '',
                                [
                                    'arn:',
                                    {
                                        'Ref': 'AWS::Partition'
                                    },
                                    ':ecr:',
                                    {
                                        'Ref': 'AWS::Region'
                                    },
                                    ':',
                                    {
                                        'Ref': 'AWS::AccountId'
                                    },
                                    ':repository/',
                                    {
                                        'Fn::Sub': 'cdk-hnb659fds-container-assets-${AWS::AccountId}-${AWS::Region}'
                                    }
                                ]
                            ]
                        }
                    },
                    {
                        'Action': 'ecr:GetAuthorizationToken',
                        'Effect': 'Allow',
                        'Resource': '*'
                    },
                    {
                        'Action': [
                            'logs:CreateLogStream',
                            'logs:PutLogEvents'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBackendFargateTaskDefnginxLogGroupDF848E6A',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': [
                            'logs:CreateLogStream',
                            'logs:PutLogEvents'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBackendFargateTaskDefApplicationContainerLogGroup789479BA',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': [
                            'secretsmanager:GetSecretValue',
                            'secretsmanager:DescribeSecret'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Ref': 'PostgresSecretAttachment5D653F4F'
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestBackendFargateTaskDefExecutionRoleDefaultPolicy531293C0',
            'Roles': [
                {
                    'Ref': 'TestBackendFargateTaskDefExecutionRoleD2B7AC7A'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'Description': 'Allow connection to Postgres instance',
            'FromPort': 5432,
            'GroupId': {
                'Fn::GetAtt': [
                    'PostgresSecurityGroupA2E13118',
                    'GroupId'
                ]
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    'TestBackendFargateServiceSecurityGroupB9C36B85',
                    'GroupId'
                ]
            },
            'ToPort': 5432
        }
    )
