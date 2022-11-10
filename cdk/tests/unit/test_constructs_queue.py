import pytest


from aws_cdk.assertions import Template


def test_constructs_queue_initialize_queue_base(stack, existing_resources):
    from infrastructure.constructs.queue import QueueProps
    from infrastructure.constructs.queue import QueueBase
    queue_base = QueueBase(
        stack,
        'QueueBase',
        props=QueueProps(
            existing_resources=existing_resources,
        )
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


def test_constructs_queue_initialize_transaction_queue(stack, existing_resources):
    from infrastructure.constructs.queue import QueueProps
    from infrastructure.constructs.queue import TransactionQueue
    transaction_queue = TransactionQueue(
        stack,
        'TransactionQueue',
        props=QueueProps(
            existing_resources=existing_resources,
        ),
    )
    assert isinstance(transaction_queue, TransactionQueue)
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::SQS::Queue',
        2
    )


def test_constructs_queue_initialize_invalidation_queue(stack, existing_resources):
    from infrastructure.constructs.queue import QueueProps
    from infrastructure.constructs.queue import InvalidationQueue
    invalidation_queue = InvalidationQueue(
        stack,
        'InvalidationQueue',
        props=QueueProps(
            existing_resources=existing_resources,
        ),
    )
    assert isinstance(invalidation_queue, InvalidationQueue)
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::SQS::Queue',
        2
    )
