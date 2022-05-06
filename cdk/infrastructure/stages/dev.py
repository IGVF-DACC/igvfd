import aws_cdk as cdk

from constructs import Construct

from infrastructure.constructs.existing import igvf_dev

from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.postgres import PostgresStack
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from typing import Any


class DevelopmentDeployStage(cdk.Stage):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.postgres_stack = PostgresStack(
            self,
            'PostgresStack',
            branch=branch,
            existing_resources_class=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
        self.backend_stack = BackendStack(
            self,
            'BackendStack',
            postgres=self.postgres_stack.postgres,
            branch=branch,
            existing_resources_class=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
