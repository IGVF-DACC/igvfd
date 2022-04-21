import aws_cdk as cdk


from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.existing import ExistingStack
from infrastructure.stacks.repository import PostgresStack
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from shared_infrastructure.cherry_lab.environments import US_WEST_2


class DevelopmentDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, branch, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.existing = ExistingStack(
            self,
            'ExistingStack',
            env=US_WEST_2,
        )
        self.vpc = self.existing.vpcs.default_vpc
        self.security_group = self.existing.security_groups.encd_demos
        self.postgres = PostgresStack(
            self,
            prepend_project_name(
                prepend_branch_name(
                    branch,
                    'PostgresStack'
                )
            ),
            vpc=self.vpc,
            security_group=self.security_group,
            branch=branch,
            env=US_WEST_2,
        )
        self.backend = BackendStack(
            self,
            prepend_project_name(
                prepend_branch_name(
                    branch,
                    'BackendStack'
                )
            ),
            vpc=self.vpc,
            security_group=self.security_group,
            postgres=self.postgres,
            branch=branch,
            env=US_WEST_2,
        )
