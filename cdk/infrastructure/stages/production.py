from aws_cdk import Stage

from constructs import Construct

from infrastructure.constructs.existing import igvf_prod

from infrastructure.config import Config

from infrastructure.tags import add_tags_to_stack

from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.opensearch import OpensearchStack
from infrastructure.stacks.postgres import PostgresStack

from typing import Any


class ProductionDeployStage(Stage):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id,  **kwargs)
        self.postgres_stack = PostgresStack(
            self,
            'PostgresStack',
            config=config,
            existing_resources_class=igvf_prod.Resources,
            env=igvf_prod.US_WEST_2,
        )
        self.opensearch_stack = OpensearchStack(
            self,
            'OpensearchStack',
            config=config,
            existing_resources_class=igvf_prod.Resources,
            env=igvf_prod.US_WEST_2,
        )
        self.backend_stack = BackendStack(
            self,
            'BackendStack',
            config=config,
            postgres_multiplexer=self.postgres_stack.multiplexer,
            opensearch_multiplexer=self.opensearch_stack.multiplexer,
            existing_resources_class=igvf_prod.Resources,
            env=igvf_prod.US_WEST_2,
        )
        add_tags_to_stack(self.postgres_stack, config)
        add_tags_to_stack(self.opensearch_stack, config)
        add_tags_to_stack(self.backend_stack, config)
