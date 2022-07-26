from constructs import Construct

from shared_infrastructure.igvf_dev.connection import CodeStarConnection
from shared_infrastructure.igvf_dev.environment import US_WEST_2 as US_WEST_2
from shared_infrastructure.igvf_dev.domain import DemoDomain
from shared_infrastructure.igvf_dev.secret import DockerHubCredentials
from shared_infrastructure.igvf_dev.network import DemoNetwork
from shared_infrastructure.igvf_dev.notification import Notification

from typing import Any

from aws_cdk.aws_sns import Topic


class Resources(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.network = DemoNetwork(
            self,
            'DemoNetwork',
        )
        self.domain = DemoDomain(
            self,
            'DemoDomain',
        )
        self.docker_hub_credentials = DockerHubCredentials(
            self,
            'DockerHubCredentials',
        )
        self.code_star_connection = CodeStarConnection(
            self,
            'CodeStarConnection',
        )
        self.notification = Notification(
            self,
            'Notification',
        )
        self.events_topic = Topic.from_topic_arn(
            self,
            'EventsTopic',
            topic_arn='arn:aws:sns:us-west-2:109189702753:EventNotificationStack-EventNotificationTopicB86E055D-1PHCT0ADKA4IJ',
        )
