import aws_cdk as cdk

from infrastructure.constructs.existing import igvf_dev

from infrastructure.config import config
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack
from infrastructure.stacks.pipeline import DemoDeploymentPipelineStack


app = cdk.App()

branch = (
    app.node.try_get_context('branch')
    or config['default_branch']
)

demo = app.node.try_get_context('demo')


def continuous_deployment_pipeline_stack():
    return ContinuousDeploymentPipelineStack(
        app,
        prepend_project_name(
            prepend_branch_name(
                branch,
                'ContinuousDeploymentPipelineStack',
            )
        ),
        branch=branch,
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )


def demo_deployment_pipeline_stack():
    return DemoDeploymentPipelineStack(
        app,
        prepend_project_name(
            prepend_branch_name(
                branch,
                'DemoDeploymentPipelineStack',
            )
        ),
        branch=branch,
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )


def pipeline_factory(branch, demo):
    if demo is not None:
        return demo_deployment_pipeline_stack()
    return continuous_deployment_pipeline_stack()


pipeline = pipeline_factory(branch, demo)


app.synth()
