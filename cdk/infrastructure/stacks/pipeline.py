import aws_cdk as cdk

from infrastructure.constructs.pipeline import ContinuousDeploymentPipeline


class ContinuousDeploymentPipelineStack(cdk.Stack):

    def __init__(self, scope, construct_id, branch, existing_resources, chatbot, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        self.existing_resources = existing_resources(
            self,
            'ExistingResources',
        )
        self.pipeline = ContinuousDeploymentPipeline(
            self,
            'ContinuousDeploymentPipeline',
            github_repo='IGVF-DACC/igvfd',
            branch=branch,
            chatbot=chatbot,
            existing_resources=self.existing_resources,
        )
