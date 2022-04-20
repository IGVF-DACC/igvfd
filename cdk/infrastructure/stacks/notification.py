import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_chatbot import SlackChannelConfiguration

from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name


class NotificationStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, branch=None, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        name = prepend_project_name(
            prepend_branch_name(
                branch,
                'aws-chatbot',
            )
        )
        self.chatbot = SlackChannelConfiguration(
            self,
            'encode-dcc-aws-chatbot',
            slack_channel_configuration_name='aws-chatbot',
            slack_workspace_id='T1KMV4JJZ',
            slack_channel_id='C034GTRCCLU',
        )
