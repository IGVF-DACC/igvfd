import aws_cdk as cdk

from constructs import Construct

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.existing.types import ExistingResourcesClass
from infrastructure.constructs.postgres import Postgres

from typing import Any


class BackendStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            postgres: Postgres,
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
            branch=branch,
            postgres=postgres,
            existing_resources=self.existing_resources,
            cpu=1024,
            memory_limit_mib=2048,
            desired_count=1,
            max_capacity=4,
        )
