import pytest


from aws_cdk.assertions import Template


def test_constructs_alarms_postgres_initialize_postgres_alarms(stack, vpc, instance_type, mocker, config, existing_resources):
    from aws_cdk.aws_rds import DatabaseInstance
    from aws_cdk.aws_rds import DatabaseInstanceEngine
    from aws_cdk.aws_rds import PostgresEngineVersion
    from aws_cdk.aws_ec2 import SubnetSelection
    from aws_cdk.aws_ec2 import SubnetType
    from infrastructure.constructs.alarms.postgres import PostgresAlarms
    from infrastructure.constructs.alarms.postgres import PostgresAlarmsProps
    database = DatabaseInstance(
        stack,
        'DatabaseInstance',
        engine=DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        ),
        vpc=existing_resources.network.vpc,
        vpc_subnets=SubnetSelection(
            subnet_type=SubnetType.PRIVATE_ISOLATED,
        ),
    )
    alarms = PostgresAlarms(
        stack,
        'PostgresAlarms',
        props=PostgresAlarmsProps(
            config=config,
            existing_resources=existing_resources,
            database=database,
        )
    )
    template = Template.from_stack(stack)
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
                    'Name': 'DBInstanceIdentifier',
                    'Value': {
                        'Ref': 'DatabaseInstance24D16791'
                    }
                }
            ],
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/RDS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 85
        }

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
                    'Name': 'DBInstanceIdentifier',
                    'Value': {
                        'Ref': 'DatabaseInstance24D16791'
                    }
                }
            ],
            'MetricName': 'FreeableMemory',
            'Namespace': 'AWS/RDS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 2000000000
        }
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
                    'Name': 'DBInstanceIdentifier',
                    'Value': {
                        'Ref': 'DatabaseInstance24D16791'
                    }
                }
            ],
            'MetricName': 'FreeStorageSpace',
            'Namespace': 'AWS/RDS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Average',
            'Threshold': 5000000000
        }
    )
    template.resource_count_is(
        'AWS::CloudWatch::Alarm',
        3
    )
