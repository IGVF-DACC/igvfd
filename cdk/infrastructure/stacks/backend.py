import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.backend import BackendProps

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
            opensearch: Opensearch,
            existing_resources_class: ExistingResourcesClass,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.backend = Backend(
            self,
            'Backend',
            props=BackendProps(
                **config.backend,
                config=config,
                existing_resources=self.existing_resources,
                postgres_multiplexer=postgres_multiplexer,
                opensearch=opensearch,
            )
        )
