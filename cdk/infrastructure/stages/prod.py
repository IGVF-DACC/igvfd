import aws_cdk as cdk

from infrastructure.stacks.backend import BackendStack


class ProdDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        BackendStack(
            self,
            'ProdBackendStack',
        )
