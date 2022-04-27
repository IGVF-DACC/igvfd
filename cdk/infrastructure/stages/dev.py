import aws_cdk as cdk

from infrastructure.constructs.existing import igvf_dev

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
            existing_resources=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
        self.backend = BackendStack(
            self,
            'BackendStack',
            postgres=self.postgres,
            branch=branch,
            existing_resources=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
