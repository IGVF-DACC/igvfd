import pytest


from aws_cdk.assertions import Template


def test_constructs_alarms_queue_initialize_queue_alarms(stack, existing_resources):
    from aws_cdk.aws_sqs import DeadLetterQueue
    from aws_cdk.aws_sqs import Queue
    from infrastructure.constructs.alarms.queue import QueueAlarmsProps
    from infrastructure.constructs.alarms.queue import QueueAlarms
    dead_letter_queue = Queue(
        stack,
        'DeadLetterQueue',
    )
    queue = Queue(
        stack,
        'Queue',
        dead_letter_queue=DeadLetterQueue(
            queue=dead_letter_queue,
            max_receive_count=3
        )
    )
    alarms = QueueAlarms(
        stack,
        'QueueAlarms',
        props=QueueAlarmsProps(
            existing_resources=existing_resources,
            queue=queue,
            dead_letter_queue=dead_letter_queue,
            oldest_message_in_seconds_threshold=600,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::CloudWatch::Alarm',
        2
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
                    'Name': 'QueueName',
                    'Value': {
                        'Fn::GetAtt': [
                            'DeadLetterQueue9F481546',
                            'QueueName'
                        ]
                    }
                }
            ],
            'MetricName': 'ApproximateNumberOfMessagesVisible',
            'Namespace': 'AWS/SQS',
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
                    'Name': 'QueueName',
                    'Value': {
                        'Fn::GetAtt': [
                            'Queue4A7E3555',
                            'QueueName'
                        ]
                    }
                }
            ],
            'MetricName': 'ApproximateAgeOfOldestMessage',
            'Namespace': 'AWS/SQS',
            'OKActions': [
                {
                    'Ref': 'TestTopic339EC197'
                }
            ],
            'Period': 300,
            'Statistic': 'Maximum',
            'Threshold': 600
        },
    )
