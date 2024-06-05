from constructs import Construct

from shared_infrastructure.igvf_sandbox.connection import CodeStarConnection
from shared_infrastructure.igvf_sandbox.environment import US_WEST_2 as US_WEST_2
from shared_infrastructure.igvf_sandbox.domain import Domain
from shared_infrastructure.igvf_sandbox.secret import DockerHubCredentials
from shared_infrastructure.igvf_sandbox.network import Network
from shared_infrastructure.igvf_sandbox.notification import Notification
from shared_infrastructure.igvf_sandbox.bus import Bus
from shared_infrastructure.igvf_sandbox.secret import PortalCredentials
from shared_infrastructure.igvf_sandbox.policy import BucketAccessPolicies
from shared_infrastructure.igvf_sandbox.secret import UploadFilesUserAccessKeys
from shared_infrastructure.igvf_sandbox.secret import UploadRestrictedFilesUserAccessKeys

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
        self.bucket_access_policies = BucketAccessPolicies(
            self,
            'BucketAccessPolicies',
        )
        self.upload_igvf_files_user_access_keys = UploadFilesUserAccessKeys(
            self,
            'UploadFilesUserAccessKeys',
        )
        self.upload_igvf_restricted_files_user_access_keys = UploadRestrictedFilesUserAccessKeys(
            self,
            'UploadRestrictedFilesUserAccessKeys',
        )
