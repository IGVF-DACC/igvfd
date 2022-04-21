import aws_cdk as cdk

from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import DeploymentCircuitBreaker
from aws_cdk.aws_ecs import Secret
from aws_cdk.aws_ecs import LogDriver

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from aws_cdk.aws_iam import ManagedPolicy

from infrastructure.constructs.existing import ExistingResources


class BackendStack(cdk.Stack):

    def __init__(self, scope, construct_id, postgres, branch, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        existing = ExistingResources(
            self,
            'ExistingResources',
        )
        application_image = ContainerImage.from_asset(
            '../',
            file='docker/pyramid/Dockerfile',

        )
        nginx_image = ContainerImage.from_asset(
            '../',
            file='docker/nginx/Dockerfile',
        )
        fargate_service = ApplicationLoadBalancedFargateService(
            self,
            'Fargate',
            vpc=existing.vpcs.default_vpc,
            cpu=1024,
            desired_count=1,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                container_name='nginx',
                image=nginx_image,
                log_driver=LogDriver.aws_logs(
                    stream_prefix='nginx',
                    mode=AwsLogDriverMode.NON_BLOCKING,
                ),
            ),
            memory_limit_mib=2048,
            public_load_balancer=True,
            security_groups=[
                existing.security_groups.encd_demos,
            ],
            assign_public_ip=True,
            certificate=existing.encd_domain.certificate,
            domain_zone=existing.encd_domain.domain_zone,
            domain_name=f'igvfd-{branch}.api.encodedcc.org',
            redirect_http=True,
        )
        fargate_service.task_definition.add_container(
            'ApplicationContainer',
            container_name='pyramid',
            image=application_image,
            environment={
                'DB_HOST': postgres.database.instance_endpoint.hostname,
                'DB_NAME': postgres.database_name,
            },
            secrets={
                'DB_PASSWORD': Secret.from_secrets_manager(
                    postgres.database.secret,
                    'password'
                ),
            },
            logging=LogDriver.aws_logs(
                stream_prefix='pyramid',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )
        fargate_service.target_group.configure_health_check(
            interval=cdk.Duration.seconds(60),
        )
        cdk.Tags.of(fargate_service).add(
            'branch',
            branch
        )
        fargate_service.task_definition.task_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMManagedInstanceCore'
            )
        )
        cfn_service = fargate_service.service.node.default_child
        cfn_service.enable_execute_command = True
        scalable_task = fargate_service.service.auto_scale_task_count(
            max_capacity=4,
        )
        scalable_task.scale_on_request_count(
            'RequestCountScaling',
            requests_per_target=600,
            target_group=fargate_service.target_group,
            scale_in_cooldown=cdk.Duration.seconds(60),
            scale_out_cooldown=cdk.Duration.seconds(60),
        )
