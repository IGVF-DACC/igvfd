import aws_cdk as cdk

from infrastructure.constructs.backend import Backend


class BackendStack(cdk.Stack):

    def __init__(self, scope, construct_id, *, branch, postgres, existing_resources, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources(
            self,
            'ExistingResources',
        )
        self.backend = Backend(
            self,
            'Backend',
            branch=branch,
            postgres=postgres,
            existing_resources=self.existing_resources,
            cpu=1024,
            memory_limit_mib=2048,
            desired_count=1,
            max_capacity=4,
        )
