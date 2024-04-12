import pytest

import json

from aws_cdk.assertions import Template


def test_constructs_tasks_deduplicatequeue(
    stack,
    config,
    existing_resources,
    application_load_balanced_fargate_service,
    invalidation_queue,
    snapshot,
):
    from infrastructure.constructs.tasks.deduplicatequeue import DeduplicateInvalidationQueue
    from infrastructure.constructs.tasks.deduplicatequeue import DeduplicateInvalidationQueueProps
    DeduplicateInvalidationQueue(
        stack,
        'Deduplicator',
        props=DeduplicateInvalidationQueueProps(
            config=config,
            existing_resources=existing_resources,
            cluster=application_load_balanced_fargate_service.cluster,
            invalidation_queue=invalidation_queue,
            number_of_workers=50,
            minutes_to_wait_between_runs=25,
            cpu=512,
            memory_limit_mib=2048,
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
        'deduplicatequeue_task_template.json'
    )
