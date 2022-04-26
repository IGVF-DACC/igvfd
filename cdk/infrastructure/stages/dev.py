import aws_cdk as cdk

from infrastructure.config import IGVF_DEV_US_WEST_2
from infrastructure.constructs.existing import IgvfDevExistingResources
from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.postgres import PostgresStack
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name


class DevelopmentDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, branch, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.postgres = PostgresStack(
            self,
            'PostgresStack',
            branch=branch,
            existing_construct=IgvfDevExistingResources,
            env=IGVF_DEV_US_WEST_2,
        )
        self.backend = BackendStack(
            self,
            'BackendStack',
            postgres=self.postgres,
            branch=branch,
            existing_construct=IgvfDevExistingResources,
            env=IGVF_DEV_US_WEST_2,
        )
