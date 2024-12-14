import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.backend import BackendProps

from infrastructure.constructs.indexer import InvalidationServiceProps
from infrastructure.constructs.indexer import IndexingServiceProps
from infrastructure.constructs.indexer import IndexerProps
from infrastructure.constructs.indexer import Indexer

from infrastructure.constructs.queue import QueueProps
from infrastructure.constructs.queue import TransactionQueue
from infrastructure.constructs.queue import InvalidationQueue
from infrastructure.constructs.queue import DeduplicationQueue

from infrastructure.constructs.flag import FeatureFlagServiceProps
from infrastructure.constructs.flag import FeatureFlagService

from infrastructure.constructs.opensearch import Opensearch

from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.multiplexer import Multiplexer

from typing import Any


class BackendStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            postgres_multiplexer: Multiplexer,
            opensearch_multiplexer: Multiplexer,
            existing_resources_class: ExistingResourcesClass,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.transaction_queue = TransactionQueue(
            self,
            'TransactionQueue',
            props=QueueProps(
                existing_resources=self.existing_resources,
            ),
        )
        self.invalidation_queue = InvalidationQueue(
            self,
            'InvalidationQueue',
            props=QueueProps(
                existing_resources=self.existing_resources,
            ),
        )
        self.deduplication_queue = DeduplicationQueue(
            self,
            'DeduplicationQueue',
            props=QueueProps(
                existing_resources=self.existing_resources,
            ),
        )
        self.feature_flag_service = FeatureFlagService(
            self,
            'FeatureFlags',
            props=FeatureFlagServiceProps(
                **config.feature_flag_service,
                config=config,
            )
        )
        self.backend = Backend(
            self,
            'Backend',
            props=BackendProps(
                **config.backend,
                config=config,
                existing_resources=self.existing_resources,
                postgres_multiplexer=postgres_multiplexer,
                opensearch_multiplexer=opensearch_multiplexer,
                transaction_queue=self.transaction_queue,
                invalidation_queue=self.invalidation_queue,
                deduplication_queue=self.deduplication_queue,
                feature_flag_service=self.feature_flag_service,
            )
        )
        self.indexer = Indexer(
            self,
            'Indexer',
            props=IndexerProps(
                config=config,
                existing_resources=self.existing_resources,
                cluster=self.backend.fargate_service.cluster,
                transaction_queue=self.transaction_queue,
                invalidation_queue=self.invalidation_queue,
                opensearch_multiplexer=opensearch_multiplexer,
                use_opensearch_named=self.backend.props.write_to_opensearch_named,
                backend_url=f'https://{self.backend.domain_name}',
                resources_index='snovault-resources',
                invalidation_service_props=InvalidationServiceProps(
                    **config.invalidation_service,
                ),
                indexing_service_props=IndexingServiceProps(
                    **config.indexing_service,
                )
            )
        )
