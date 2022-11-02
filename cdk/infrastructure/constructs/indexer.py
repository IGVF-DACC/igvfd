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

from infrastructure.constructs.opensearch import Opensearch

from infrastructure.constructs.queue import TransactionQueue
from infrastructure.constructs.queue import InvalidationQueue

from infrastructure.constructs.existing.types import ExistingResources

from typing import Any

from dataclasses import dataclass


@dataclass
class IndexerProps:
    config: Config
    existing_resources: ExistingResources
    cluster: ICluster
    transaction_queue: TransactionQueue
    invalidation_queue: InvalidationQueue
    opensearch: Opensearch
    backend_url: str
    resources_index: str


class Indexer(Construct):

    props: IndexerProps
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
        self._define_docker_assets()
        self._define_invalidation_service()
        self._allow_invalidation_service_to_write_to_invalidation_queue()
        self._define_portal_credentials()
        self._define_indexing_service()
        self._allow_connections_to_opensearch()

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
            cpu=256,
            memory_limit_mib=512,
            min_scaling_capacity=1,
            max_scaling_capacity=2,
            scaling_steps=[
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
                )
            ],
            enable_execute_command=True,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            environment={
                'OPENSEARCH_URL': self.props.opensearch.url,
                'TRANSACTION_QUEUE_URL': self.props.transaction_queue.queue.queue_url,
                'INVALIDATION_QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
                'RESOURCES_INDEX': self.props.resources_index,
            },
            command=['run-invalidation-service'],
            log_driver=LogDriver.aws_logs(
                stream_prefix='invalidation-service',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
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
            cpu=256,
            memory_limit_mib=512,
            min_scaling_capacity=1,
            max_scaling_capacity=2,
            scaling_steps=[
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
                )
            ],
            enable_execute_command=True,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            environment={
                'INVALIDATION_QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
                'OPENSEARCH_URL': self.props.opensearch.url,
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

    def _allow_connections_to_opensearch(self) -> None:
        self.invalidation_service.service.connections.allow_to(
            self.props.opensearch.domain,
            Port.tcp(443),
            description='Allow connection to Opensearch',
        )
        self.indexing_service.service.connections.allow_to(
            self.props.opensearch.domain,
            Port.tcp(443),
            description='Allow connection to Opensearch',
        )
