import pytest


from aws_cdk.assertions import Template


def test_constructs_waf_initialize_waf(stack, vpc, existing_resources, config):
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ec2 import SubnetSelection
    from aws_cdk.aws_ec2 import SubnetType
    from infrastructure.constructs.waf import WAFProps
    from infrastructure.constructs.waf import WAF
    fargate_service = ApplicationLoadBalancedFargateService(
        stack,
        'FargateService',

        task_image_options=ApplicationLoadBalancedTaskImageOptions(
            image=ContainerImage.from_registry('some-test')
        ),
    )
    waf = WAF(
        stack,
        'WAF',
        props=WAFProps(
            enabled=True,
            arn='some-waf-arn',
            alb=fargate_service.load_balancer,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::WAFv2::WebACLAssociation',
        1
    )


def test_constructs_waf_initialize_waf_disabled(stack, vpc, existing_resources, config):
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ec2 import SubnetSelection
    from aws_cdk.aws_ec2 import SubnetType
    from infrastructure.constructs.waf import WAFProps
    from infrastructure.constructs.waf import WAF
    fargate_service = ApplicationLoadBalancedFargateService(
        stack,
        'FargateService',

        task_image_options=ApplicationLoadBalancedTaskImageOptions(
            image=ContainerImage.from_registry('some-test')
        ),
    )
    waf = WAF(
        stack,
        'WAF',
        props=WAFProps(
            enabled=False,
            arn='some-waf-arn',
            alb=fargate_service.load_balancer,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::WAFv2::WebACLAssociation',
        0
    )


def test_constructs_waf_initialize_waf_no_arn(stack, vpc, existing_resources, config):
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ec2 import SubnetSelection
    from aws_cdk.aws_ec2 import SubnetType
    from infrastructure.constructs.waf import WAFProps
    from infrastructure.constructs.waf import WAF
    fargate_service = ApplicationLoadBalancedFargateService(
        stack,
        'FargateService',

        task_image_options=ApplicationLoadBalancedTaskImageOptions(
            image=ContainerImage.from_registry('some-test')
        ),
    )
    waf = WAF(
        stack,
        'WAF',
        props=WAFProps(
            enabled=True,
            arn='',
            alb=fargate_service.load_balancer,
        )
    )
    template = Template.from_stack(stack)
    template.resource_count_is(
        'AWS::WAFv2::WebACLAssociation',
        0
    )
