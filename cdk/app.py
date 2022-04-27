import aws_cdk as cdk

from infrastructure.constructs.existing import igvf_dev

from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


app = cdk.App()

branch = (
    app.node.try_get_context('branch')
    or config.get('default_branch')
)

pipeline = ContinuousDeploymentPipelineStack(
    app,
    prepend_project_name(
        prepend_branch_name(
            branch,
            'ContinuousDeploymentPipelineStack',
        )
    ),
    branch=branch,
    existing_resources=igvf_dev.Resources,
    env=igvf_dev.US_WEST_2,
)

app.synth()
