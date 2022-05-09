import aws_cdk as cdk

from constructs import Construct

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
        )


class DemoDeploymentPipelineStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            existing_resources_class: ExistingResourcesClass,
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
        )
