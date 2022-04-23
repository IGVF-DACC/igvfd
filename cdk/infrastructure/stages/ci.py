import aws_cdk as cdk

from infrastructure.stacks.ci import ContinuousIntegrationStack

from infrastructure.config import IGVF_DEV_US_WEST_2


class CIDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        ContinuousIntegrationStack(
            self,
            'ContinuousIntegrationStack',
            env=IGVF_DEV_US_WEST_2,
        )
