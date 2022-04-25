import aws_cdk as cdk

from infrastructure.config import IGVF_DEV_US_WEST_2
from infrastructure.constructs.existing import IgvfDevExistingResources
from infrastructure.stacks.ci import ContinuousIntegrationStack


class CIDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        ContinuousIntegrationStack(
            self,
            'ContinuousIntegrationStack',
            existing_construct=IgvfDevExistingResources,
            env=IGVF_DEV_US_WEST_2,
        )
