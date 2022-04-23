from constructs import Construct

from aws_cdk.aws_certificatemanager import Certificate

from aws_cdk.aws_ec2 import Vpc

from aws_cdk.aws_route53 import HostedZone


class IgvfDevDomain(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.certificate = Certificate.from_certificate_arn(
            self,
            'DomainCertificate',
            'arn:aws:acm:us-west-2:109189702753:certificate/6bee1171-2028-43eb-aab8-d992da3c60df'
        )
        self.domain_name = 'demo.igvf.org'
        self.domain_zone = HostedZone.from_lookup(
            self,
            'DomainZone',
            domain_name=self.domain_name,
        )


class ExistingResources(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.igvf_dev_vpc = Vpc.from_lookup(
            self,
            'IgvfDevVpc',
            vpc_id='vpc-0b5e3b97317057133'
        )
        self.igvf_dev_domain = IgvfDevDomain(
            self,
            'IgvfDevDomain',
        )
