from constructs import Construct

from shared_infrastructure.igvf_dev.connection import CodeStarConnection
from shared_infrastructure.igvf_dev.environment import US_WEST_2 as US_WEST_2
from shared_infrastructure.igvf_dev.domain import DemoDomain
from shared_infrastructure.igvf_dev.secret import DockerHubCredentials
from shared_infrastructure.igvf_dev.network import DemoNetwork
from shared_infrastructure.igvf_dev.notification import Notification
from shared_infrastructure.igvf_dev.bus import Bus
from shared_infrastructure.igvf_dev.secret import PortalCredentials
from shared_infrastructure.igvf_dev.policy import BucketAccessPolicies

from typing import Any


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
        self.portal_credentials = PortalCredentials(
            self,
            'PortalCredentials',
        )
        self.code_star_connection = CodeStarConnection(
            self,
            'CodeStarConnection',
        )
        self.notification = Notification(
            self,
            'Notification',
        )
        self.bus = Bus(
            self,
            'Bus',
        )
        self.bucket_access_policies = BucketAccessPolicies(
            self,
            'BucketAccessPolicies',
        )
