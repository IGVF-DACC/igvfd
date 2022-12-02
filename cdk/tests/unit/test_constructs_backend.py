import pytest

from aws_cdk.assertions import Template


def test_constructs_backend_initialize_backend_construct(
        stack,
        instance_type,
        existing_resources,
        vpc,
        config,
        opensearch,
        transaction_queue,
        invalidation_queue,
):
    from infrastructure.constructs.backend import Backend
    from infrastructure.constructs.backend import BackendProps
    from infrastructure.constructs.postgres import Postgres
    from infrastructure.constructs.postgres import PostgresProps
    from infrastructure.multiplexer import Multiplexer
    from infrastructure.multiplexer import MultiplexerConfig
    # Given
    postgres_multiplexer = Multiplexer(
        stack,
        configs=[
            MultiplexerConfig(
                construct_id='Postgres',
                on=True,
                construct_class=Postgres,
                kwargs={
                    'props': PostgresProps(
                        config=config,
                        existing_resources=existing_resources,
                        allocated_storage=10,
                        max_allocated_storage=20,
                        instance_type=instance_type
                    )
                }
            ),
        ]
    )
    # When
    backend = Backend(
        stack,
        'TestBackend',
        props=BackendProps(
            config=config,
            existing_resources=existing_resources,
            postgres_multiplexer=postgres_multiplexer,
            opensearch=opensearch,
            transaction_queue=transaction_queue,
            invalidation_queue=invalidation_queue,
            cpu=2048,
            memory_limit_mib=4096,
            desired_count=4,
            max_capacity=7,
            ini_name='demo.ini',
            use_postgres_named='Postgres'
        )
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
            'ServiceName': 'Backend',
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
                        },
                        {
                            'Name': 'INI_NAME',
                            'Value': 'demo.ini'
                        },
                        {
                            'Name': 'SESSION_COOKIE_DOMAIN',
                            'Value': 'my.test.domain.org'
                        },
                        {
                            'Name': 'DEFAULT_EVENT_BUS',
                            'Value': {
                                'Fn::GetAtt': [
                                    'TestBusF2C65FE8',
                                    'Arn'
                                ]
                            }
                        },
                        {
                            'Name': 'EVENT_SOURCE',
                            'Value': 'igvfd.demo.some-branch'
                        },
                        {
                            'Name': 'OPENSEARCH_URL',
                            'Value': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'https://',
                                        {
                                            'Fn::GetAtt': [
                                                'OpensearchDomainCED7C974',
                                                'DomainEndpoint'
                                            ]
                                        }
                                    ]
                                ]
                            }
                        },
                        {
                            'Name': 'TRANSACTION_QUEUE_URL',
                            'Value': {
                                'Ref': 'TransactionQueueE05C979B'
                            }
                        },
                        {
                            'Name': 'INVALIDATION_QUEUE_URL',
                            'Value': {
                                'Ref': 'InvalidationQueue8614463D'
                            }
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
                        },
                        {
                            'Name': 'SESSION_SECRET',
                            'ValueFrom': {
                                'Ref': 'TestBackendSessionSecret012661FA'
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
                    },
                    {
                        'Action': [
                            'secretsmanager:GetSecretValue',
                            'secretsmanager:DescribeSecret'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Ref': 'TestBackendSessionSecret012661FA'
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
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': 'events:PutEvents',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBusF2C65FE8',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': [
                            'sqs:SendMessage',
                            'sqs:GetQueueAttributes',
                            'sqs:GetQueueUrl'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TransactionQueueE05C979B',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': [
                            'sqs:SendMessage',
                            'sqs:GetQueueAttributes',
                            'sqs:GetQueueUrl'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'InvalidationQueue8614463D',
                                'Arn'
                            ]
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestBackendFargateTaskDefTaskRoleDefaultPolicyF2A9F228',
            'Roles': [
                {
                    'Ref': 'TestBackendFargateTaskDefTaskRoleD1640BC4'
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
    template.has_resource_properties(
        'AWS::Events::Rule',
        {
            'EventPattern': {
                'detail-type': [
                    'UpgradeFolderChanged'
                ],
                'source': [
                    'igvfd.demo.some-branch'
                ]
            },
            'State': 'ENABLED',
            'Targets': [
                {
                    'Arn': {
                        'Fn::GetAtt': [
                            'EcsDefaultClusterMnL3mNNYNTestVpc4872C696',
                            'Arn'
                        ]
                    },
                    'EcsParameters': {
                        'LaunchType': 'FARGATE',
                        'NetworkConfiguration': {
                            'AwsVpcConfiguration': {
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
                        'TaskCount': 1,
                        'TaskDefinitionArn': {
                            'Ref': 'TestBackendFargateTaskDef9FA612FC'
                        }
                    },
                    'Id': 'Target0',
                    'Input': '{\"containerOverrides\":[{\"name\":\"pyramid\",\"command\":[\"/scripts/pyramid/batchupgrade-with-notification.sh\"]},{\"name\":\"nginx\",\"command\":[\"sleep\",\"3600\"]}]}',
                    'RoleArn': {
                        'Fn::GetAtt': [
                            'TestBackendFargateTaskDefEventsRoleADEEE321',
                            'Arn'
                        ]
                    }
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': 'eventbridge:PutEvents',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBusF2C65FE8',
                                'Arn'
                            ]
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestBackendBatchUpgradePutUpgradeFolderChangedEventCustomResourcePolicy83C269FA',
            'Roles': [
                {
                    'Ref': 'AWS679f53fac002430cb0da5b7982bd2287ServiceRoleC1EA0FF2'
                }
            ]
        }
    )
    template.has_resource_properties(
        'Custom::AWS',
        {
            'ServiceToken': {
                'Fn::GetAtt': [
                    'AWS679f53fac002430cb0da5b7982bd22872D164C4C',
                    'Arn'
                ]
            },
            'InstallLatestAwsSdk': True
        }
    )
    template.has_resource_properties(
        'AWS::Events::Rule',
        {
            'EventPattern': {
                'detail-type': [
                    'MappingChanged'
                ],
                'source': [
                    'igvfd.demo.some-branch'
                ]
            },
            'State': 'ENABLED',
            'Targets': [
                {
                    'Arn': {
                        'Fn::GetAtt': [
                            'EcsDefaultClusterMnL3mNNYNTestVpc4872C696',
                            'Arn'
                        ]
                    },
                    'EcsParameters': {
                        'LaunchType': 'FARGATE',
                        'NetworkConfiguration': {
                            'AwsVpcConfiguration': {
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
                        'TaskCount': 1,
                        'TaskDefinitionArn': {
                            'Ref': 'TestBackendFargateTaskDef9FA612FC'
                        }
                    },
                    'Id': 'Target0',
                    'Input': '{\"containerOverrides\":[{\"name\":\"pyramid\",\"command\":[\"/scripts/pyramid/delete-and-create-mapping-and-reindex.sh\"]},{\"name\":\"nginx\",\"command\":[\"sleep\",\"3600\"]}]}',
                    'RoleArn': {
                        'Fn::GetAtt': [
                            'TestBackendFargateTaskDefEventsRoleADEEE321',
                            'Arn'
                        ]
                    }
                }
            ]
        }
    )
    template.has_resource_properties(
        'Custom::AWS',
        {
            'ServiceToken': {
                'Fn::GetAtt': [
                    'AWS679f53fac002430cb0da5b7982bd22872D164C4C',
                    'Arn'
                ]
            },
            'InstallLatestAwsSdk': True
        }
    )
