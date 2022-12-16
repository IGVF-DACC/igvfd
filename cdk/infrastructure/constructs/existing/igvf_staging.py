from constructs import Construct

from shared_infrastructure.igvf_staging.connection import CodeStarConnection
from shared_infrastructure.igvf_staging.environment import US_WEST_2 as US_WEST_2
from shared_infrastructure.igvf_staging.domain import Domain
from shared_infrastructure.igvf_staging.secret import DockerHubCredentials
from shared_infrastructure.igvf_staging.network import Network
from shared_infrastructure.igvf_staging.notification import Notification
from shared_infrastructure.igvf_staging.bus import Bus
from shared_infrastructure.igvf_staging.secret import PortalCredentials

from typing import Any


class Resources(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.network = Network(
            self,
            'Network',
        )
        self.domain = Domain(
            self,
            'Domain',
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
