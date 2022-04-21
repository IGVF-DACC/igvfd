from constructs import Construct

from aws_cdk.aws_certificatemanager import Certificate

from aws_cdk.aws_route53 import HostedZone

from shared_infrastructure.cherry_lab.security_groups import SecurityGroups
from shared_infrastructure.cherry_lab.vpcs import VPCs


class ENCDDomain(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.certificate = Certificate.from_certificate_arn(
            self,
            'DomainCertificate',
            'arn:aws:acm:us-west-2:618537831167:certificate/6e16fc50-1206-48fa-b14a-13d97cb1fee6'
        )
        self.domain_zone = HostedZone.from_lookup(
            self,
            'DomainZone',
            domain_name='api.encodedcc.org'
        )


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
        self.encd_domain = ENCDDomain(
            self,
            'ENCDDomain',
        )
