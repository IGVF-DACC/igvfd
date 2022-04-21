import aws_cdk as cdk

from infrastructure.stacks.backend import BackendStack
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from shared_infrastructure.cherry_lab.environments import US_WEST_2


class DevelopmentDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, branch=None, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        backend = BackendStack(
            self,
            prepend_project_name(
                prepend_branch_name(
                    branch,
                    'BackendStack'
                )
            ),
            env=US_WEST_2,
            branch=branch,
        )
