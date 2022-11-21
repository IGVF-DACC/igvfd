import pytest


from aws_cdk.assertions import Template


def test_constructs_alarms_indexer_initialize_invalidation_service_alarms(
        stack,
        existing_resources,
        queue_processing_fargate_service
):
    from infrastructure.constructs.alarms.indexer import InvalidationServiceAlarmsProps
    from infrastructure.constructs.alarms.indexer import InvalidationServiceAlarms
    alarms = InvalidationServiceAlarms(
        stack,
        'InvalidationServiceAlarams',
        props=InvalidationServiceAlarmsProps(
            existing_resources=existing_resources,
            fargate_service=queue_processing_fargate_service,
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CloudWatch::Alarm',
        {
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'EvaluationPeriods': 2,
            'AlarmActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Dimensions': [
                {
                    'Name': 'ClusterName',
                    'Value': {
                        'Ref': 'EcsDefaultClusterMnL3mNNYNTestVpc4872C696'
                    }
                },
                {
                    'Name': 'ServiceName',
                    'Value': {
                        'Fn::GetAtt': [
                            'QueueProcessingFargateService3C60BF26',
                            'Name'
                        ]
                    }
                }
            ],
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/ECS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 85
        },
    )
    template.has_resource_properties(
        'AWS::CloudWatch::Alarm',
        {
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'EvaluationPeriods': 1,
            'AlarmActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Dimensions': [
                {
                    'Name': 'ClusterName',
                    'Value': {
                        'Ref': 'EcsDefaultClusterMnL3mNNYNTestVpc4872C696'
                    }
                },
                {
                    'Name': 'ServiceName',
                    'Value': {
                        'Fn::GetAtt': [
                            'QueueProcessingFargateService3C60BF26',
                            'Name'
                        ]
                    }
                }
            ],
            'MetricName': 'MemoryUtilization',
            'Namespace': 'AWS/ECS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 80
        },
    )


def test_constructs_alarms_indexer_initialize_indexing_service_alarms(
        stack,
        existing_resources,
        queue_processing_fargate_service
):
    from infrastructure.constructs.alarms.indexer import IndexingServiceAlarmsProps
    from infrastructure.constructs.alarms.indexer import IndexingServiceAlarms
    alarms = IndexingServiceAlarms(
        stack,
        'IndexingServiceAlarams',
        props=IndexingServiceAlarmsProps(
            existing_resources=existing_resources,
            fargate_service=queue_processing_fargate_service,
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CloudWatch::Alarm',
        {
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'EvaluationPeriods': 2,
            'AlarmActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Dimensions': [
                {
                    'Name': 'ClusterName',
                    'Value': {
                        'Ref': 'EcsDefaultClusterMnL3mNNYNTestVpc4872C696'
                    }
                },
                {
                    'Name': 'ServiceName',
                    'Value': {
                        'Fn::GetAtt': [
                            'QueueProcessingFargateService3C60BF26',
                            'Name'
                        ]
                    }
                }
            ],
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/ECS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 85
        },
    )
    template.has_resource_properties(
        'AWS::CloudWatch::Alarm',
        {
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'EvaluationPeriods': 1,
            'AlarmActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Dimensions': [
                {
                    'Name': 'ClusterName',
                    'Value': {
                        'Ref': 'EcsDefaultClusterMnL3mNNYNTestVpc4872C696'
                    }
                },
                {
                    'Name': 'ServiceName',
                    'Value': {
                        'Fn::GetAtt': [
                            'QueueProcessingFargateService3C60BF26',
                            'Name'
                        ]
                    }
                }
            ],
            'MetricName': 'MemoryUtilization',
            'Namespace': 'AWS/ECS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 80
        },
    )
