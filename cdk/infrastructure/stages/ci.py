import aws_cdk as cdk

from infrastructure.stacks.ci import ContinuousIntegrationStack


class CIDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        ContinuousIntegrationStack(
            self,
            'ContinuousIntegrationStack'
        )
