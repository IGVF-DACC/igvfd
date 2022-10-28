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

from infrastructure.constructs.alarms.backend import BackendAlarmsProps
from infrastructure.constructs.alarms.backend import BackendAlarms

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.opensearch import Opensearch

from infrastructure.constructs.postgres import PostgresConstruct

from infrastructure.constructs.queue import InvalidationQueue
from infrastructure.constructs.queue import TransactionQueue

from infrastructure.constructs.tasks.batchupgrade import BatchUpgrade
from infrastructure.constructs.tasks.batchupgrade import BatchUpgradeProps

from infrastructure.constructs.tasks.updatemapping import UpdateMapping
from infrastructure.constructs.tasks.updatemapping import UpdateMappingProps

from infrastructure.events.naming import get_event_source_from_config

from infrastructure.multiplexer import Multiplexer

from typing import Any
from typing import cast

from dataclasses import dataclass


@dataclass
class BackendProps:
    config: Config
    existing_resources: ExistingResources
    postgres_multiplexer: Multiplexer
    opensearch: Opensearch
    transaction_queue: TransactionQueue
    invalidation_queue: InvalidationQueue
    cpu: int
    memory_limit_mib: int
    desired_count: int
    max_capacity: int
    use_postgres_named: str


class Backend(Construct):

    props: BackendProps
    postgres: PostgresConstruct
    application_image: ContainerImage
    domain_name: str
    nginx_image: ContainerImage
    fargate_service: ApplicationLoadBalancedFargateService
    batch_upgrade: BatchUpgrade

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
        self._define_postgres()
        self._generate_session_secret()
        self._define_docker_assets()
        self._define_domain_name()
        self._define_fargate_service()
        self._add_application_container_to_task()
        self._allow_connections_to_database()
        self._allow_connections_to_opensearch()
        self._allow_task_to_put_events_on_bus()
        self._allow_task_to_send_messages_to_transaction_queue()
        self._allow_task_to_send_messages_to_invalidation_queue()
        self._configure_health_check()
        self._add_tags_to_fargate_service()
        self._enable_exec_command()
        self._configure_task_scaling()
        self._run_batch_upgrade_automatically()
        self._run_update_mapping_automatically()
        self._add_alarms()

    def _define_postgres(self) -> None:
        self.postgres = cast(
            PostgresConstruct,
            self.props.postgres_multiplexer.resources.get(
                self.props.use_postgres_named
            )
        )

    def _define_docker_assets(self) -> None:
        self.application_image = ContainerImage.from_asset(
            '../',
            file='docker/pyramid/Dockerfile',

        )
        self.nginx_image = ContainerImage.from_asset(
            '../',
            file='docker/nginx/Dockerfile',
        )

    def _define_domain_name(self) -> None:
        self.domain_name = (
            f'igvfd-{self.props.config.branch}.{self.props.existing_resources.domain.name}'
        )

    def _define_fargate_service(self) -> None:
        self.fargate_service = ApplicationLoadBalancedFargateService(
            self,
            'Fargate',
            service_name='Portal',
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
            domain_name=self.domain_name,
            redirect_http=True,
        )

    def _get_database_secret(self) -> Secret:
        database_secret = self.postgres.database.secret
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
        self.fargate_service.task_definition.add_container(
            'ApplicationContainer',
            container_name=container_name,
            image=self.application_image,
            environment={
                'DB_HOST': self.postgres.database.instance_endpoint.hostname,
                'DB_NAME': self.postgres.database_name,
                'DEFAULT_EVENT_BUS': self.props.existing_resources.bus.default.event_bus_arn,
                'EVENT_SOURCE': get_event_source_from_config(self.props.config),
                'OPENSEARCH_URL': self.props.opensearch.url,
                'TRANSACTION_QUEUE_URL': self.props.transaction_queue.queue.queue_url,
                'INVALIDATION_QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
            },
            secrets={
                'DB_PASSWORD': self._get_database_secret(),
                'SESSION_SECRET': self._get_session_secret(),
            },
            logging=LogDriver.aws_logs(
                stream_prefix=container_name,
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )

    def _allow_connections_to_database(self) -> None:
        self.fargate_service.service.connections.allow_to(
            self.postgres.database,
            Port.tcp(5432),
            description='Allow connection to Postgres instance',
        )

    def _allow_connections_to_opensearch(self) -> None:
        self.fargate_service.service.connections.allow_to(
            self.props.opensearch.domain,
            Port.tcp(443),
            description='Allow connection to Opensearch',
        )

    def _allow_task_to_put_events_on_bus(self) -> None:
        self.props.existing_resources.bus.default.grant_put_events_to(
            self.fargate_service.task_definition.task_role
        )

    def _allow_task_to_send_messages_to_transaction_queue(self) -> None:
        self.props.transaction_queue.queue.grant_send_messages(
            self.fargate_service.task_definition.task_role
        )

    def _allow_task_to_send_messages_to_invalidation_queue(self) -> None:
        self.props.invalidation_queue.queue.grant_send_messages(
            self.fargate_service.task_definition.task_role
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

    def _run_batch_upgrade_automatically(self) -> None:
        self.batch_upgrade = BatchUpgrade(
            self,
            'BatchUpgrade',
            props=BatchUpgradeProps(
                config=self.props.config,
                existing_resources=self.props.existing_resources,
                fargate_service=self.fargate_service,
            )
        )

    def _run_update_mapping_automatically(self) -> None:
        self.update_mapping = UpdateMapping(
            self,
            'UpdateMapping',
            props=UpdateMappingProps(
                config=self.props.config,
                existing_resources=self.props.existing_resources,
                fargate_service=self.fargate_service,
            )
        )

    def _add_alarms(self) -> None:
        BackendAlarms(
            self,
            'BackendAlarms',
            props=BackendAlarmsProps(
                config=self.props.config,
                existing_resources=self.props.existing_resources,
                fargate_service=self.fargate_service
            )
        )
