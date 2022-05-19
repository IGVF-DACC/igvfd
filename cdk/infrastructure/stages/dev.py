import aws_cdk as cdk

from constructs import Construct

from infrastructure.constructs.existing import igvf_dev

from infrastructure.config import Config
from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.postgres import PostgresStack

from typing import Any


class DevelopmentDeployStage(cdk.Stage):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.postgres_stack = PostgresStack(
            self,
            'PostgresStack',
            config=config,
            existing_resources_class=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
        self.backend_stack = BackendStack(
            self,
            'BackendStack',
            config=config,
            postgres=self.postgres_stack.postgres,
            existing_resources_class=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
