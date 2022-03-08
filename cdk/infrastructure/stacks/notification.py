import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_chatbot import SlackChannelConfiguration

from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name


class NotificationStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, branch= None, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        name = prepend_project_name(
            prepend_branch_name(
                branch,
                'aws-chatbot',
            )
        )
        self.chatbot = SlackChannelConfiguration.from_slack_channel_configuration_arn(
            self,
            name,
            slack_channel_configuration_arn=(
                'arn:aws:chatbot::618537831167:chat-configuration/slack-channel/aws-chatbot'
            )
        )
