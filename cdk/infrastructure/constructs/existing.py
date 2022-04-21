from constructs import Construct

from shared_infrastructure.cherry_lab.security_groups import SecurityGroups
from shared_infrastructure.cherry_lab.vpcs import VPCs


class ExistingResources(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.vpcs = VPCs(
            self,
            'VPCs',
        )
        self.security_groups = SecurityGroups(
            self,
            'SecurityGroups',
        )
