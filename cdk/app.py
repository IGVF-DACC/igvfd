import aws_cdk as cdk
import igvfd
import os

from infrastructure.config import config
from infrastructure.naming import prepend_project_name

from infrastructure.stacks.backend import BackendStack
from infrastructure.stacks.notification import NotificationStack
from infrastructure.stacks.pipeline import NotificationStack


ENVIRONMENT = cdk.Environment(
    account=config['account'],
    region=config['region'],
)

BRANCH = app.node.try_get_context('branch') or config.get('default_branch')

app = cdk.App()

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

pipeline = CdkPipelineStack(
    app,
    prepend_project_name(
        'CdkPipelineStack'
    ),
    chatbot=notification.chatbot,
    branch=BRANCH,
    env=ENVIRONMENT,
)

app.synth()
