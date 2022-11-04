import pytest


from aws_cdk.assertions import Template


def test_constructs_queue_initialize_queue_base(stack):
    from infrastructure.constructs.queue import QueueBase
    queue_base = QueueBase(
        stack,
        'QueueBase',
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::SQS::Queue',
        2
    )
    template.has_resource_properties(
        'AWS::SQS::Queue',
        {
            'MessageRetentionPeriod': 1209600
        }
    )
    template.has_resource_properties(
        'AWS::SQS::Queue',
        {
            'RedrivePolicy': {
                'deadLetterTargetArn': {
                    'Fn::GetAtt': [
                        'QueueBaseDeadLetterQueueDF9C28E1',
                        'Arn'
                    ]
                },
                'maxReceiveCount': 3
            },
            'VisibilityTimeout': 120
        }
    )


def test_constructs_queue_initialize_transaction_queue(stack):
    from infrastructure.constructs.queue import TransactionQueue
    transaction_queue = TransactionQueue(
        stack,
        'TransactionQueue',
    )
    assert isinstance(transaction_queue, TransactionQueue)
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::SQS::Queue',
        2
    )


def test_constructs_queue_initialize_invalidation_queue(stack):
    from infrastructure.constructs.queue import InvalidationQueue
    invalidation_queue = InvalidationQueue(
        stack,
        'InvalidationQueue',
    )
    assert isinstance(invalidation_queue, InvalidationQueue)
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::SQS::Queue',
        2
    )
