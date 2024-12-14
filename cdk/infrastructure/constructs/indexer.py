from constructs import Construct

from aws_cdk.aws_applicationautoscaling import ScalingInterval

from aws_cdk.aws_ec2 import Port

from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import ICluster
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import DeploymentCircuitBreaker
from aws_cdk.aws_ecs import Secret
from aws_cdk.aws_ecs import LogDriver

from aws_cdk.aws_ecs_patterns import QueueProcessingFargateService

from aws_cdk.aws_secretsmanager import Secret as SMSecret
from aws_cdk.aws_secretsmanager import ISecret

from infrastructure.config import Config

from infrastructure.constructs.alarms.indexer import InvalidationServiceAlarmsProps
from infrastructure.constructs.alarms.indexer import InvalidationServiceAlarms
from infrastructure.constructs.alarms.indexer import IndexingServiceAlarmsProps
from infrastructure.constructs.alarms.indexer import IndexingServiceAlarms

from infrastructure.constructs.opensearch import Opensearch

from infrastructure.constructs.queue import TransactionQueue
from infrastructure.constructs.queue import InvalidationQueue
from infrastructure.constructs.queue import DeduplicationQueue

from infrastructure.constructs.tasks.deduplicatequeue import DeduplicateInvalidationQueue
from infrastructure.constructs.tasks.deduplicatequeue import DeduplicateInvalidationQueueProps

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.multiplexer import Multiplexer

from typing import Any
from typing import cast
from typing import List

from dataclasses import dataclass
from dataclasses import field


@dataclass
class InvalidationServiceProps:
    cpu: int
    memory_limit_mib: int
    min_scaling_capacity: int
    max_scaling_capacity: int
    scaling_steps: List[ScalingInterval] = field(
        default_factory=lambda: [
            ScalingInterval(
                upper=0,
                change=-1,
            ),
            ScalingInterval(
                lower=1,
                change=1,
            ),
            ScalingInterval(
                lower=1000,
                change=2,
            ),
        ]
    )


@dataclass
class IndexingServiceProps:
    cpu: int
    memory_limit_mib: int
    min_scaling_capacity: int
    max_scaling_capacity: int
    scaling_steps: List[ScalingInterval] = field(
        default_factory=lambda: [
            ScalingInterval(
                upper=0,
                change=-1,
            ),
            ScalingInterval(
                lower=1,
                change=1,
            ),
            ScalingInterval(
                lower=1000,
                change=2,
            ),
        ]
    )


@dataclass
class IndexerProps:
    config: Config
    existing_resources: ExistingResources
    cluster: ICluster
    transaction_queue: TransactionQueue
    invalidation_queue: InvalidationQueue
    deduplication_queue: DeduplicationQueue
    opensearch_multiplexer: Multiplexer
    use_opensearch_named: str
    backend_url: str
    resources_index: str
    invalidation_service_props: InvalidationServiceProps
    indexing_service_props: IndexingServiceProps


class Indexer(Construct):

    props: IndexerProps
    opensearch: Opensearch
    services_image: ContainerImage
    invalidation_service: QueueProcessingFargateService
    indexing_service: QueueProcessingFargateService
    portal_credentials: ISecret

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: IndexerProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_opensearch()
        self._define_docker_assets()
        self._define_invalidation_service()
        self._remove_cpu_scaling_from_invalidation_service()
        self._allow_invalidation_service_to_write_to_invalidation_queue()
        self._define_portal_credentials()
        self._define_indexing_service()
        self._remove_cpu_scaling_from_indexing_service()
        self._allow_invalidation_service_to_connect_to_opensearch()
        self._allow_indexing_service_to_connect_to_opensearch()
        self._add_alarms_to_invalidation_service()
        self._add_alarms_to_indexing_service()
        self._run_deduplicate_invalidation_queue_automatically()

    def _define_opensearch(self) -> None:
        self.opensearch = cast(
            Opensearch,
            self.props.opensearch_multiplexer.resources.get(
                self.props.use_opensearch_named,
            )
        )

    def _define_docker_assets(self) -> None:
        self.services_image = ContainerImage.from_asset(
            '../docker/snoindex',
        )

    def _define_invalidation_service(self) -> None:
        self.invalidation_service = QueueProcessingFargateService(
            self,
            'InvalidationService',
            service_name='InvalidationService',
            image=self.services_image,
            cluster=self.props.cluster,
            queue=self.props.transaction_queue.queue,
            assign_public_ip=True,
            cpu=self.props.invalidation_service_props.cpu,
            memory_limit_mib=self.props.invalidation_service_props.memory_limit_mib,
            min_scaling_capacity=self.props.invalidation_service_props.min_scaling_capacity,
            max_scaling_capacity=self.props.invalidation_service_props.max_scaling_capacity,
            scaling_steps=self.props.invalidation_service_props.scaling_steps,
            enable_execute_command=True,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            environment={
                'OPENSEARCH_URL': self.opensearch.url,
                'TRANSACTION_QUEUE_URL': self.props.transaction_queue.queue.queue_url,
                'INVALIDATION_QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
                'RESOURCES_INDEX': self.props.resources_index,
            },
            command=['run-bulk-invalidation-service'],
            log_driver=LogDriver.aws_logs(
                stream_prefix='invalidation-service',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )

    def _remove_cpu_scaling_from_invalidation_service(self) -> None:
        self.invalidation_service.service.node.find_child(
            'TaskCount'
        ).node.find_child(
            'Target'
        ).node.try_remove_child(
            'CpuScaling'
        )

    def _allow_invalidation_service_to_write_to_invalidation_queue(self) -> None:
        self.props.invalidation_queue.queue.grant_send_messages(
            self.invalidation_service.task_definition.task_role
        )

    def _define_portal_credentials(self) -> None:
        self.portal_credentials = self.props.existing_resources.portal_credentials.indexing_service_key

    def _define_indexing_service(self) -> None:
        self.indexing_service = QueueProcessingFargateService(
            self,
            'IndexingService',
            service_name='IndexingService',
            image=self.services_image,
            cluster=self.props.cluster,
            queue=self.props.invalidation_queue.queue,
            assign_public_ip=True,
            cpu=self.props.indexing_service_props.cpu,
            memory_limit_mib=self.props.indexing_service_props.memory_limit_mib,
            min_scaling_capacity=self.props.indexing_service_props.min_scaling_capacity,
            max_scaling_capacity=self.props.indexing_service_props.max_scaling_capacity,
            scaling_steps=self.props.indexing_service_props.scaling_steps,
            enable_execute_command=True,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            environment={
                'INVALIDATION_QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
                'OPENSEARCH_URL': self.opensearch.url,
                'RESOURCES_INDEX': self.props.resources_index,
                'BACKEND_URL': self.props.backend_url,
            },
            secrets={
                'BACKEND_KEY': Secret.from_secrets_manager(
                    self.portal_credentials,
                    'BACKEND_KEY',
                ),
                'BACKEND_SECRET_KEY': Secret.from_secrets_manager(
                    self.portal_credentials,
                    'BACKEND_SECRET_KEY',
                )
            },
            command=['run-indexing-service'],
            log_driver=LogDriver.aws_logs(
                stream_prefix='indexing-service',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )

    def _remove_cpu_scaling_from_indexing_service(self) -> None:
        self.indexing_service.service.node.find_child(
            'TaskCount'
        ).node.find_child(
            'Target'
        ).node.try_remove_child(
            'CpuScaling'
        )

    def _allow_invalidation_service_to_connect_to_opensearch(self) -> None:
        self.invalidation_service.service.connections.allow_to(
            self.opensearch.domain,
            Port.tcp(443),
            description='Allow connection to Opensearch',
        )

    def _allow_indexing_service_to_connect_to_opensearch(self) -> None:
        self.indexing_service.service.connections.allow_to(
            self.opensearch.domain,
            Port.tcp(443),
            description='Allow connection to Opensearch',
        )

    def _add_alarms_to_invalidation_service(self) -> None:
        InvalidationServiceAlarms(
            self,
            'InvalidationServiceAlarms',
            props=InvalidationServiceAlarmsProps(
                existing_resources=self.props.existing_resources,
                fargate_service=self.invalidation_service,
            )
        )

    def _add_alarms_to_indexing_service(self) -> None:
        IndexingServiceAlarms(
            self,
            'IndexingServiceAlarms',
            props=IndexingServiceAlarmsProps(
                existing_resources=self.props.existing_resources,
                fargate_service=self.indexing_service,
            )
        )

    def _run_deduplicate_invalidation_queue_automatically(self) -> None:
        DeduplicateInvalidationQueue(
            self,
            'DedupIQ',  # Avoid hitting length limit in SG details.
            props=DeduplicateInvalidationQueueProps(
                config=self.props.config,
                existing_resources=self.props.existing_resources,
                cluster=self.props.cluster,
                invalidation_queue=self.props.invalidation_queue,
                deduplication_queue=self.props.deduplication_queue,
                number_of_workers=100,
                minutes_to_wait_between_runs=60,
                cpu=1024,
                memory_limit_mib=2048,
            )
        )
