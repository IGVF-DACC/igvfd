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

from aws_cdk.aws_secretsmanager import Secret as SMSecret
from aws_cdk.aws_secretsmanager import SecretStringGenerator

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.postgres import PostgresConstruct

from typing import Any
from typing import cast

from dataclasses import dataclass

from aws_cdk.aws_cloudwatch import Alarm
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk import Duration
from aws_cdk.aws_elasticloadbalancingv2 import HttpCodeTarget
from aws_cdk.aws_logs import ILogGroup, LogGroup, FilterPattern
from aws_cdk.aws_ecs import AwsLogDriver


@dataclass
class BackendProps:
    config: Config
    existing_resources: ExistingResources
    postgres: PostgresConstruct
    cpu: int
    memory_limit_mib: int
    desired_count: int
    max_capacity: int


class Backend(Construct):

    props: BackendProps
    application_image: ContainerImage
    nginx_image: ContainerImage
    fargate_service: ApplicationLoadBalancedFargateService

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: BackendProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._generate_session_secret()
        self._define_docker_assets()
        self._define_fargate_service()
        self._add_application_container_to_task()
        self._allow_connections_to_database()
        self._configure_health_check()
        self._add_tags_to_fargate_service()
        self._enable_exec_command()
        self._configure_task_scaling()
        self._add_metric_alarms()

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
            vpc=self.props.existing_resources.network.vpc,
            cpu=self.props.cpu,
            desired_count=self.props.desired_count,
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
            memory_limit_mib=self.props.memory_limit_mib,
            public_load_balancer=True,
            assign_public_ip=True,
            certificate=self.props.existing_resources.domain.certificate,
            domain_zone=self.props.existing_resources.domain.zone,
            domain_name=f'igvfd-{self.props.config.branch}.{self.props.existing_resources.domain.name}',
            redirect_http=True,
        )

    def _get_database_secret(self) -> Secret:
        database_secret = self.props.postgres.database.secret
        # Unwrap optional for mypy.
        if database_secret is None:
            raise ValueError('Database secret is None')
        return Secret.from_secrets_manager(
            database_secret,
            'password'
        )

    def _generate_session_secret(self) -> None:
        self.session_secret = SMSecret(
            self,
            'SessionSecret',
            generate_secret_string=SecretStringGenerator(
                password_length=128
            )
        )

    def _get_session_secret(self) -> Secret:
        return Secret.from_secrets_manager(
            self.session_secret
        )

    def _add_application_container_to_task(self) -> None:
        container_name = 'pyramid'
        self.pyramid_log_group = LogGroup(
            self,
            'PyramidLogGroup',
        )
        self.pyramid_log_driver = AwsLogDriver.aws_logs(
            stream_prefix=container_name,
            mode=AwsLogDriverMode.NON_BLOCKING,
            log_group=self.pyramid_log_group,
        )
        self.fargate_service.task_definition.add_container(
            'ApplicationContainer',
            container_name=container_name,
            image=self.application_image,
            environment={
                'DB_HOST': self.props.postgres.database.instance_endpoint.hostname,
                'DB_NAME': self.props.postgres.database_name,
            },
            secrets={
                'DB_PASSWORD': self._get_database_secret(),
                'SESSION_SECRET': self._get_session_secret(),
            },
            logging=self.pyramid_log_driver
        )

    def _allow_connections_to_database(self) -> None:
        self.fargate_service.service.connections.allow_to(
            self.props.postgres.database,
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
            self.props.config.branch
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
            max_capacity=self.props.max_capacity,
        )
        scalable_task.scale_on_request_count(
            'RequestCountScaling',
            requests_per_target=600,
            target_group=self.fargate_service.target_group,
            scale_in_cooldown=cdk.Duration.seconds(60),
            scale_out_cooldown=cdk.Duration.seconds(60),
        )

    def _add_metric_alarms(self) -> None:
        events_topic_action = SnsAction(
            self.props.existing_resources.events_topic
        )

        cpu_alarm = self.fargate_service.service.metric_cpu_utilization().create_alarm(
            self,
            'FargateServiceCPUAlarm',
            evaluation_periods=1,
            threshold=50,
        )
        cpu_alarm.add_alarm_action(
            events_topic_action,
        )
        cpu_alarm.add_ok_action(
            events_topic_action,
        )

        memory_alarm = self.fargate_service.service.metric_memory_utilization().create_alarm(
            self,
            'FargateServiceMemoryAlarm',
            evaluation_periods=1,
            threshold=12,
        )
        memory_alarm.add_alarm_action(
            events_topic_action
        )
        memory_alarm.add_ok_action(
            events_topic_action
        )

        target_group_request_count_alarm = self.fargate_service.target_group.metric_request_count(
            period=Duration.minutes(1)
        ).create_alarm(
            self,
            'FargateServiceTargetGroupRequestCountAlarm',
            evaluation_periods=1,
            threshold=30,
        )
        target_group_request_count_alarm.add_alarm_action(
            events_topic_action
        )
        target_group_request_count_alarm.add_ok_action(
            events_topic_action
        )

        target_group_response_time_alarm = self.fargate_service.target_group.metric_target_response_time(
            period=Duration.minutes(5)
        ).create_alarm(
            self,
            'FargateServiceTargetGroupResponseTime',
            evaluation_periods=1,
            threshold=1,
        )
        target_group_response_time_alarm.add_alarm_action(
            events_topic_action
        )
        target_group_response_time_alarm.add_ok_action(
            events_topic_action
        )

        load_balancer_500_error_response_alarm = self.fargate_service.load_balancer.metric_http_code_target(
            code=HttpCodeTarget.TARGET_5XX_COUNT,
        ).create_alarm(
            self,
            'FargateServiceLoadBalancer500Alarm',
            evaluation_periods=1,
            threshold=10
        )
        load_balancer_500_error_response_alarm.add_alarm_action(
            events_topic_action
        )
        load_balancer_500_error_response_alarm.add_ok_action(
            events_topic_action
        )
