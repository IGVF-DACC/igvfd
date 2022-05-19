import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.backend import BackendProps

from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.constructs.postgres import PostgresConstruct

from typing import Any


class BackendStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            postgres: PostgresConstruct,
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
                config=config,
                existing_resources=self.existing_resources,
                postgres=postgres,
                cpu=1024,
                memory_limit_mib=2048,
                desired_count=1,
                max_capacity=4,
            )
        )
