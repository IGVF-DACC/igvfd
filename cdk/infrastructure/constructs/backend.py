import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_ec2 import Port

from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import CfnService
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import DeploymentCircuitBreaker
from aws_cdk.aws_ecs import Secret
from aws_cdk.aws_ecs import LogDriver

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from aws_cdk.aws_iam import ManagedPolicy

from infrastructure.constructs.existing.types import ExistingResources
from infrastructure.constructs.postgres import Postgres

from typing import Any
from typing import cast


class Backend(Construct):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            postgres: Postgres,
            existing_resources: ExistingResources,
            cpu: int,
            memory_limit_mib: int,
            desired_count: int,
            max_capacity: int,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._branch = branch
        self._postgres = postgres
        self._existing_resources = existing_resources
        self._cpu = cpu
        self._memory_limit_mib = memory_limit_mib
        self._desired_count = desired_count
        self._max_capacity = max_capacity
        self._define_docker_assets()
        self._define_fargate_service()
        self._add_application_container_to_task()
        self._allow_connections_to_database()
        self._configure_health_check()
        self._add_tags_to_fargate_service()
        self._enable_exec_command()
        self._configure_task_scaling()

    def _define_docker_assets(self) -> None:
        self.application_image = ContainerImage.from_asset(
            '../',
            file='docker/pyramid/Dockerfile',

        )
        self.nginx_image = ContainerImage.from_asset(
            '../',
            file='docker/nginx/Dockerfile',
        )

    def _define_fargate_service(self) -> None:
        self.fargate_service = ApplicationLoadBalancedFargateService(
            self,
            'Fargate',
            vpc=self._existing_resources.network.vpc,
            cpu=self._cpu,
            desired_count=self._desired_count,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                container_name='nginx',
                image=self.nginx_image,
                log_driver=LogDriver.aws_logs(
                    stream_prefix='nginx',
                    mode=AwsLogDriverMode.NON_BLOCKING,
                ),
            ),
            memory_limit_mib=self._memory_limit_mib,
            public_load_balancer=True,
            assign_public_ip=True,
            certificate=self._existing_resources.domain.certificate,
            domain_zone=self._existing_resources.domain.zone,
            domain_name=f'igvfd-{self._branch}.{self._existing_resources.domain.name}',
            redirect_http=True,
        )

    def _get_database_secret(self) -> Secret:
        database_secret = self._postgres.database.secret
        # Unwrap optional for mypy.
        if database_secret is None:
            raise ValueError('Database secret is None')
        return Secret.from_secrets_manager(
            database_secret,
            'password'
        )

    def _add_application_container_to_task(self) -> None:
        container_name = 'pyramid'
        self.fargate_service.task_definition.add_container(
            'ApplicationContainer',
            container_name=container_name,
            image=self.application_image,
            environment={
                'DB_HOST': self._postgres.database.instance_endpoint.hostname,
                'DB_NAME': self._postgres.database_name,
            },
            secrets={
                'DB_PASSWORD': self._get_database_secret(),
            },
            logging=LogDriver.aws_logs(
                stream_prefix=container_name,
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )

    def _allow_connections_to_database(self) -> None:
        self.fargate_service.service.connections.allow_to(
            self._postgres.database,
            Port.tcp(5432),
            description='Allow connection to Postgres instance',
        )

    def _configure_health_check(self) -> None:
        self.fargate_service.target_group.configure_health_check(
            interval=cdk.Duration.seconds(60),
        )

    def _add_tags_to_fargate_service(self) -> None:
        cdk.Tags.of(self.fargate_service).add(
            'branch',
            self._branch
        )

    def _enable_exec_command(self) -> None:
        self.fargate_service.task_definition.task_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMManagedInstanceCore'
            )
        )
        # Make mypy happy (default child is Optional[IConstruct]).
        cfn_service = cast(
            CfnService,
            self.fargate_service.service.node.default_child
        )
        cfn_service.enable_execute_command = True

    def _configure_task_scaling(self) -> None:
        scalable_task = self.fargate_service.service.auto_scale_task_count(
            max_capacity=self._max_capacity,
        )
        scalable_task.scale_on_request_count(
            'RequestCountScaling',
            requests_per_target=600,
            target_group=self.fargate_service.target_group,
            scale_in_cooldown=cdk.Duration.seconds(60),
            scale_out_cooldown=cdk.Duration.seconds(60),
        )
