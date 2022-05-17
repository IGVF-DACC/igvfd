import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.pipeline import ContinuousDeploymentPipeline
from infrastructure.constructs.pipeline import DemoDeploymentPipeline

from infrastructure.constructs.existing.types import ExistingResourcesClass

from typing import Any


class ContinuousDeploymentPipelineStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            existing_resources_class: ExistingResourcesClass,
            config: Config,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id,  **kwargs)
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.pipeline = ContinuousDeploymentPipeline(
            self,
            'ContinuousDeploymentPipeline',
            github_repo='IGVF-DACC/igvfd',
            branch=branch,
            existing_resources=self.existing_resources,
            config=config,
        )


class DemoDeploymentPipelineStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            existing_resources_class: ExistingResourcesClass,
            config: Config,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id,  **kwargs)
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.pipeline = DemoDeploymentPipeline(
            self,
            'DemoDeploymentPipeline',
            github_repo='IGVF-DACC/igvfd',
            branch=branch,
            existing_resources=self.existing_resources,
            config=config,
        )


pipeline_stacks = [
    ContinuousDeploymentPipelineStack,
    DemoDeploymentPipelineStack,
]


name_to_pipeline_stack_map = {
    pipeline_stack.__name__: pipeline_stack
    for pipeline_stack in pipeline_stacks
}


def pipeline_stack_factory(name: str):
    return name_to_pipeline_stack_map[name]
