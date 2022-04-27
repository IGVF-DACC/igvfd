import aws_cdk as cdk

from infrastructure.constructs.existing import igvf_dev

from infrastructure.stacks.ci import ContinuousIntegrationStack


class CIDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        ContinuousIntegrationStack(
            self,
            'ContinuousIntegrationStack',
            existing_resources=igvf_dev.Resources,
            env=igvf_dev.US_WEST_2,
        )
