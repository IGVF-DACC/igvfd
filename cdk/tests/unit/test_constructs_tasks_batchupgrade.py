import pytest

from aws_cdk.assertions import Template


def test_constructs_tasks_batchupgrade_initialize_batchupgrade(stack, mocker, config, existing_resources):
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
    from infrastructure.constructs.tasks.batchupgrade import BatchUpgrade
    from infrastructure.constructs.tasks.batchupgrade import BatchUpgradeProps
    fargate_service = ApplicationLoadBalancedFargateService(
        stack,
        'TestApplicationLoadBalancedFargateService',
        vpc=existing_resources.network.vpc,
        assign_public_ip=True,
        task_image_options=ApplicationLoadBalancedTaskImageOptions(
            image=ContainerImage.from_registry('some-test-image')
        ),
    )
    batchupgrade = BatchUpgrade(
        stack,
        'TestBatchUpgrade',
        props=BatchUpgradeProps(
            config=config,
            existing_resources=existing_resources,
            fargate_service=fargate_service,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::ECS::Service',
        1
    )
    template.resource_count_is(
        'AWS::ECS::Cluster',
        1
    )
    template.resource_count_is(
        'AWS::ECS::TaskDefinition',
        1
    )
    template.resource_count_is(
        'AWS::Events::Rule',
        1
    )
