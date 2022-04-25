from constructs import Construct

from aws_cdk.aws_certificatemanager import Certificate

from aws_cdk.aws_ec2 import Vpc

from aws_cdk.aws_route53 import HostedZone

from aws_cdk.aws_secretsmanager import Secret


class IgvfDevDomain(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.certificate = Certificate.from_certificate_arn(
            self,
            'DomainCertificate',
            'arn:aws:acm:us-west-2:109189702753:certificate/6bee1171-2028-43eb-aab8-d992da3c60df'
        )
        self.name = 'demo.igvf.org'
        self.zone = HostedZone.from_lookup(
            self,
            'DomainZone',
            domain_name=self.name,
        )


class IgvfDevCredentials(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.docker_credentials = Secret.from_secret_complete_arn(
            self,
            'DockerSecret',
            'arn:aws:secretsmanager:us-west-2:109189702753:secret:docker-hub-credentials-EStRH5',
        )


class IgvfDevCodeStarConnection:

    def __init__(self):
        self.arn = (
            'arn:aws:codestar-connections:'
            'us-west-2:109189702753:'
            'connection/d65802e7-37d9-4be6-bc86-f94b2104b5ff'
        )


class ExistingResources(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)


class IgvfDevExistingResources(ExistingResources):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = Vpc.from_lookup(
            self,
            'IgvfDevVpc',
            vpc_id='vpc-0b5e3b97317057133'
        )
        self.domain = IgvfDevDomain(
            self,
            'IgvfDevDomain',
        )
        self.credentials = IgvfDevCredentials(
            self,
            'IgvfDevCredentials',
        )
        self.code_star_connection = IgvfDevCodeStarConnection()
