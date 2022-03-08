import aws_cdk as cdk
import igvfd
import os

from infrastructure.config import config
from infrastructure.naming import prepend_project_name

from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.notification import NotificationStack
from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


ENVIRONMENT = cdk.Environment(
    account=config['account'],
    region=config['region'],
)

app = cdk.App()

branch = (
    app.node.try_get_context('branch')
    or config.get('default_branch')
)

backend = BackendStack(
    app,
    prepend_project_name(
        'BackendStack'
    ),
    env=ENVIRONMENT,
)

notification = NotificationStack(
    app,
    prepend_project_name(
        'NotificationStack'
    ),
    env=ENVIRONMENT,
)

pipeline = ContinuousDeploymentPipelineStack(
    app,
    prepend_project_name(
        'ContinuousDeploymentPipelineStack'
    ),
    chatbot=notification.chatbot,
    branch=branch,
    env=ENVIRONMENT,
)

app.synth()
