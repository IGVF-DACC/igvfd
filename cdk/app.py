import aws_cdk as cdk

from infrastructure.config import IGVF_DEV_US_WEST_2
from infrastructure.constructs.existing import IgvfDevExistingResources
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name
from infrastructure.stacks.notification import NotificationStack
from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


app = cdk.App()

branch = (
    app.node.try_get_context('branch')
    or config.get('default_branch')
)

notification = NotificationStack(
    app,
    prepend_project_name(
        prepend_branch_name(
            branch,
            'NotificationStack',
        )
    ),
    branch=branch,
    env=IGVF_DEV_US_WEST_2,
)

pipeline = ContinuousDeploymentPipelineStack(
    app,
    prepend_project_name(
        prepend_branch_name(
            branch,
            'ContinuousDeploymentPipelineStack',
        )
    ),
    chatbot=notification.chatbot,
    branch=branch,
    existing_construct=IgvfDevExistingResources,
    env=IGVF_DEV_US_WEST_2,
)

app.synth()
