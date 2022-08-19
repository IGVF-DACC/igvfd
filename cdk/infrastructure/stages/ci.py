import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.tags import add_tags_to_stack

from infrastructure.constructs.existing import igvf_dev

from infrastructure.stacks.ci import ContinuousIntegrationStack

from typing import Any


class CIDeployStage(cdk.Stage):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id,  **kwargs)
        self.ci = ContinuousIntegrationStack(
            self,
            'ContinuousIntegrationStack',
            existing_resources_class=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
        add_tags_to_stack(self.ci, config)
