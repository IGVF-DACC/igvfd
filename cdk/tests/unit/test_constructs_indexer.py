import pytest

from aws_cdk.assertions import Template


def test_constructs_indexer_initialize_indexer(
        stack,
        config,
        existing_resources,
        application_load_balanced_fargate_service,
        transaction_queue,
        invalidation_queue,
        opensearch_multiplexer,
):
    from infrastructure.constructs.indexer import InvalidationServiceProps
    from infrastructure.constructs.indexer import IndexingServiceProps
    from infrastructure.constructs.indexer import IndexerProps
    from infrastructure.constructs.indexer import Indexer
    indexer = Indexer(
        stack,
        'Indexer',
        props=IndexerProps(
            config=config,
            existing_resources=existing_resources,
            cluster=application_load_balanced_fargate_service.cluster,
            transaction_queue=transaction_queue,
            invalidation_queue=invalidation_queue,
            opensearch_multiplexer=opensearch_multiplexer,
            use_opensearch_named='Opensearch',
            backend_url='some-url.test',
            resources_index='some-resources-index',
            invalidation_service_props=InvalidationServiceProps(
                **config.invalidation_service,
            ),
            indexing_service_props=IndexingServiceProps(
                **config.indexing_service,
            )
        )
    )
    template = Template.from_stack(stack)
    assert isinstance(indexer, Indexer)
    template.resource_count_is(
        'AWS::SQS::Queue',
        4,
    )
    template.has_resource_properties(
        'AWS::SQS::Queue',
        {
            'RedrivePolicy': {
                'deadLetterTargetArn': {
                    'Fn::GetAtt': [
                        'TransactionQueueDeadLetterQueueDA53F160',
                        'Arn'
                    ]
                },
                'maxReceiveCount': 10
            },
            'VisibilityTimeout': 120
        }
    )
    template.has_resource_properties(
        'AWS::SQS::Queue',
        {
            'RedrivePolicy': {
                'deadLetterTargetArn': {
                    'Fn::GetAtt': [
                        'InvalidationQueueDeadLetterQueueFE5C594E',
                        'Arn'
                    ]
                },
                'maxReceiveCount': 10
            },
            'VisibilityTimeout': 120
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'Description': 'Allow connection to Opensearch',
            'FromPort': 443,
            'GroupId': {
                'Fn::GetAtt': [
                    'OpensearchDomainSecurityGroup046A436D',
                    'GroupId'
                ]
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    'IndexerIndexingServiceQueueProcessingFargateServiceSecurityGroup9D88A792',
                    'GroupId'
                ]
            },
            'ToPort': 443
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'Description': 'Allow connection to Opensearch',
            'FromPort': 443,
            'GroupId': {
                'Fn::GetAtt': [
                    'OpensearchDomainSecurityGroup046A436D',
                    'GroupId'
                ]
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    'IndexerInvalidationServiceQueueProcessingFargateServiceSecurityGroupB0C75422',
                    'GroupId'
                ]
            },
            'ToPort': 443
        }
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
            'EnableECSManagedTags': False,
            'EnableExecuteCommand': True,
            'LaunchType': 'FARGATE',
            'NetworkConfiguration': {
                'AwsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',
                    'SecurityGroups': [
                        {
                            'Fn::GetAtt': [
                                'IndexerInvalidationServiceQueueProcessingFargateServiceSecurityGroupB0C75422',
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
            'ServiceName': 'InvalidationService',
            'TaskDefinition': {
                'Ref': 'IndexerInvalidationServiceQueueProcessingTaskDefAD9C4E3C'
            }
        }
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
            'EnableECSManagedTags': False,
            'EnableExecuteCommand': True,
            'LaunchType': 'FARGATE',
            'NetworkConfiguration': {
                'AwsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',
                    'SecurityGroups': [
                        {
                            'Fn::GetAtt': [
                                'IndexerIndexingServiceQueueProcessingFargateServiceSecurityGroup9D88A792',
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
            'ServiceName': 'IndexingService',
            'TaskDefinition': {
                'Ref': 'IndexerIndexingServiceQueueProcessingTaskDef248DB181'
            }
        }
    )
    template.has_resource_properties(
        'AWS::ECS::TaskDefinition',
        {
            'ContainerDefinitions': [
                {
                    'Command': [
                        'run-bulk-invalidation-service'
                    ],
                    'Environment': [
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
                        },
                        {
                            'Name': 'RESOURCES_INDEX',
                            'Value': 'some-resources-index'
                        },
                        {
                            'Name': 'QUEUE_NAME',
                            'Value': {
                                'Fn::GetAtt': [
                                    'TransactionQueueE05C979B',
                                    'QueueName'
                                ]
                            }
                        }
                    ],
                    'Essential': True,
                    'Image': {
                    },
                    'LogConfiguration': {
                        'LogDriver': 'awslogs',
                        'Options': {
                            'awslogs-group': {
                                'Ref': 'IndexerInvalidationServiceQueueProcessingTaskDefQueueProcessingContainerLogGroup7A19AA4F'
                            },
                            'awslogs-stream-prefix': 'invalidation-service',
                            'awslogs-region': {
                                'Ref': 'AWS::Region'
                            },
                            'mode': 'non-blocking'
                        }
                    },
                    'Name': 'QueueProcessingContainer'
                }
            ],
            'Cpu': '256',
            'ExecutionRoleArn': {
                'Fn::GetAtt': [
                    'IndexerInvalidationServiceQueueProcessingTaskDefExecutionRole7CBAB82A',
                    'Arn'
                ]
            },
            'Family': 'IndexerInvalidationServiceQueueProcessingTaskDef5AA84E8A',
            'Memory': '512',
            'NetworkMode': 'awsvpc',
            'RequiresCompatibilities': [
                'FARGATE'
            ],
            'TaskRoleArn': {
                'Fn::GetAtt': [
                    'IndexerInvalidationServiceQueueProcessingTaskDefTaskRole1C46CA69',
                    'Arn'
                ]
            }
        }
    )
    template.has_resource_properties(
        'AWS::ECS::TaskDefinition',
        {
            'ContainerDefinitions': [
                {
                    'Command': [
                        'run-indexing-service'
                    ],
                    'Environment': [
                        {
                            'Name': 'INVALIDATION_QUEUE_URL',
                            'Value': {
                                'Ref': 'InvalidationQueue8614463D'
                            }
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
                            'Name': 'RESOURCES_INDEX',
                            'Value': 'some-resources-index'
                        },
                        {
                            'Name': 'BACKEND_URL',
                            'Value': 'some-url.test'
                        },
                        {
                            'Name': 'QUEUE_NAME',
                            'Value': {
                                'Fn::GetAtt': [
                                    'InvalidationQueue8614463D',
                                    'QueueName'
                                ]
                            }
                        }
                    ],
                    'Essential': True,
                    'Image': {
                    },
                    'LogConfiguration': {
                        'LogDriver': 'awslogs',
                        'Options': {
                            'awslogs-group': {
                                'Ref': 'IndexerIndexingServiceQueueProcessingTaskDefQueueProcessingContainerLogGroupE85BD506'
                            },
                            'awslogs-stream-prefix': 'indexing-service',
                            'awslogs-region': {
                                'Ref': 'AWS::Region'
                            },
                            'mode': 'non-blocking'
                        }
                    },
                    'Name': 'QueueProcessingContainer',
                    'Secrets': [
                        {
                            'Name': 'BACKEND_KEY',
                            'ValueFrom': {
                                'Fn::Join': [
                                    '',
                                    [
                                        {
                                            'Ref': 'TestSecret16AF87B1'
                                        },
                                        ':BACKEND_KEY::'
                                    ]
                                ]
                            }
                        },
                        {
                            'Name': 'BACKEND_SECRET_KEY',
                            'ValueFrom': {
                                'Fn::Join': [
                                    '',
                                    [
                                        {
                                            'Ref': 'TestSecret16AF87B1'
                                        },
                                        ':BACKEND_SECRET_KEY::'
                                    ]
                                ]
                            }
                        }
                    ]
                }
            ],
            'Cpu': '256',
            'ExecutionRoleArn': {
                'Fn::GetAtt': [
                    'IndexerIndexingServiceQueueProcessingTaskDefExecutionRoleCFBD9590',
                    'Arn'
                ]
            },
            'Family': 'IndexerIndexingServiceQueueProcessingTaskDefE0CF9535',
            'Memory': '512',
            'NetworkMode': 'awsvpc',
            'RequiresCompatibilities': [
                'FARGATE'
            ],
            'TaskRoleArn': {
                'Fn::GetAtt': [
                    'IndexerIndexingServiceQueueProcessingTaskDefTaskRoleAFEF8974',
                    'Arn'
                ]
            }
        }
    )
    template.resource_count_is(
        'AWS::ApplicationAutoScaling::ScalingPolicy',
        4
    )
    template.resource_count_is(
        'AWS::CloudWatch::Alarm',
        18
    )
    cpu_scaling_resources = template.find_resources(
        'AWS::ApplicationAutoScaling::ScalingPolicy',
        {
            'Properties': {
                'PolicyType': 'TargetTrackingScaling',
                'TargetTrackingScalingPolicyConfiguration': {
                    'PredefinedMetricSpecification': {
                        'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
                    },
                    'TargetValue': 50
                }
            }
        }
    )
    assert len(cpu_scaling_resources) == 0
    template.has_resource_properties(
        'AWS::ApplicationAutoScaling::ScalingPolicy',
        {
            'PolicyName': 'IndexerInvalidationServiceQueueProcessingFargateServiceTaskCountTargetQueueMessagesVisibleScalingLowerPolicyA4356389',
            'PolicyType': 'StepScaling',
            'ScalingTargetId': {
                'Ref': 'IndexerInvalidationServiceQueueProcessingFargateServiceTaskCountTargetE5561481'
            },
            'StepScalingPolicyConfiguration': {
                'AdjustmentType': 'ChangeInCapacity',
                'MetricAggregationType': 'Maximum',
                'StepAdjustments': [
                    {
                        'MetricIntervalUpperBound': 0,
                        'ScalingAdjustment': -1
                    }
                ]
            }
        }
    )


def test_constructs_indexer_indexer_match_snapshot(
    stack,
    config,
    existing_resources,
    application_load_balanced_fargate_service,
    transaction_queue,
    invalidation_queue,
    opensearch_multiplexer,
    snapshot,
):
    import json
    from infrastructure.constructs.indexer import InvalidationServiceProps
    from infrastructure.constructs.indexer import IndexingServiceProps
    from infrastructure.constructs.indexer import IndexerProps
    from infrastructure.constructs.indexer import Indexer
    indexer = Indexer(
        stack,
        'Indexer',
        props=IndexerProps(
            config=config,
            existing_resources=existing_resources,
            cluster=application_load_balanced_fargate_service.cluster,
            transaction_queue=transaction_queue,
            invalidation_queue=invalidation_queue,
            opensearch_multiplexer=opensearch_multiplexer,
            use_opensearch_named='Opensearch',
            backend_url='some-url.test',
            resources_index='some-resources-index',
            invalidation_service_props=InvalidationServiceProps(
                **config.invalidation_service,
            ),
            indexing_service_props=IndexingServiceProps(
                **config.indexing_service,
            )
        )
    )
    template = Template.from_stack(stack)
    template_json = template.to_json()
    snapshot.assert_match(
        json.dumps(
            template_json,
            indent=4,
            sort_keys=True
        ),
        'indexer_constructs_template.json'
    )
