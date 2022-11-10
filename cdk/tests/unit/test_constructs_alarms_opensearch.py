import pytest


from aws_cdk.assertions import Template


def test_constructs_alarms_opensearch_initialize_opensearch_alarms(stack, existing_resources):
    from aws_cdk.aws_opensearchservice import CapacityConfig
    from aws_cdk.aws_opensearchservice import Domain
    from aws_cdk.aws_opensearchservice import EngineVersion
    from aws_cdk.aws_opensearchservice import EbsOptions
    from aws_cdk.aws_opensearchservice import LoggingOptions
    from aws_cdk.aws_opensearchservice import ZoneAwarenessConfig
    from infrastructure.constructs.alarms.opensearch import OpensearchAlarmsProps
    from infrastructure.constructs.alarms.opensearch import OpensearchAlarms
    volume_size = 10
    domain = Domain(
        stack,
        'Domain',
        version=EngineVersion.OPENSEARCH_1_2,
        capacity=CapacityConfig(
            data_node_instance_type='t3.small.search',
            data_nodes=1,
        ),
        ebs=EbsOptions(
            volume_size=volume_size
        ),
    )
    alarms = OpensearchAlarms(
        stack,
        'OpenSearchAlarms',
        props=OpensearchAlarmsProps(
            existing_resources=existing_resources,
            domain=domain,
            volume_size=volume_size,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::CloudWatch::Alarm',
        6
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
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'MetricName': 'ClusterStatus.red',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Maximum',
            'Threshold': 1
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
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'MetricName': 'ClusterIndexWritesBlocked',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 60,
            'Statistic': 'Maximum',
            'Threshold': 1
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
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Maximum',
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
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'MetricName': 'JVMMemoryPressure',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Maximum',
            'Threshold': 90
        },
    )
    template.has_resource_properties(
        'AWS::CloudWatch::Alarm',
        {
            'ComparisonOperator': 'LessThanOrEqualToThreshold',
            'EvaluationPeriods': 1,
            'AlarmActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Dimensions': [
                {
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'MetricName': 'FreeStorageSpace',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Minimum',
            'Threshold': 2560
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
                    'Name': 'ClientId',
                    'Value': {
                        'Ref': 'AWS::AccountId'
                    }
                },
                {
                    'Name': 'DomainName',
                    'Value': {
                        'Ref': 'Domain66AC69E0'
                    }
                }
            ],
            'ExtendedStatistic': 'p99',
            'MetricName': 'SearchLatency',
            'Namespace': 'AWS/ES',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Threshold': 1000
        },
    )
