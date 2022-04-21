import aws_cdk as cdk

from aws_cdk.aws_certificatemanager import Certificate

from aws_cdk.aws_ec2 import SecurityGroup
from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_ecs import AssetImageProps
from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import DeploymentCircuitBreaker
from aws_cdk.aws_ecs import Secret
from aws_cdk.aws_ecs import LogDriver


from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions

from aws_cdk.aws_iam import ManagedPolicy

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion

from aws_cdk.aws_route53 import HostedZone

from constructs import Construct

from shared_infrastructure.cherry_lab.vpcs import VPCs


class BackendStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, branch=None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpcs = VPCs(
            self,
            'VPCs'
        )
        security_group = SecurityGroup.from_security_group_id(
            self,
            'encd_sg',
            'sg-022ea667',
            mutable=False
        )
        engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )
        database_name = 'igvfd'
        database = DatabaseInstance(
            self,
            'Postgres',
            database_name=database_name,
            engine=engine,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
            vpc=vpcs.default_vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PUBLIC,
            ),
            allocated_storage=10,
            max_allocated_storage=20,
            security_groups=[
                security_group,
            ],
        )
        application_image = ContainerImage.from_asset(
            '../',
            file='./docker/pyramid/Dockerfile',

        )
        nginx_image = ContainerImage.from_asset(
            '../',
            file='./docker/nginx/Dockerfile',
        )
        fargate_service = ApplicationLoadBalancedFargateService(
            self,
            'Fargate',
            vpc=vpcs.default_vpc,
            cpu=1024,
            desired_count=1,
            circuit_breaker=DeploymentCircuitBreaker(
                rollback=True,
            ),
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                container_name='nginx',
                image=nginx_image,
                log_driver=LogDriver.aws_logs(
                    stream_prefix='nginx',
                    mode=AwsLogDriverMode.NON_BLOCKING,
                ),
            ),
            memory_limit_mib=2048,
            public_load_balancer=True,
            security_groups=[
                security_group,
            ],
            assign_public_ip=True,
            certificate=Certificate.from_certificate_arn(
                self,
                'DomainCertificate',
                'arn:aws:acm:us-west-2:618537831167:certificate/6e16fc50-1206-48fa-b14a-13d97cb1fee6'
            ),
            domain_zone=HostedZone.from_lookup(
                self,
                'DomainZone',
                domain_name='api.encodedcc.org'
            ),
            domain_name=f'igvfd-{branch}.api.encodedcc.org',
            redirect_http=True,
        )
        application_container = fargate_service.task_definition.add_container(
            'ApplicationContainer',
            container_name='pyramid',
            image=application_image,
            environment={
                'DB_HOST': database.instance_endpoint.hostname,
                'DB_NAME': database_name,
            },
            secrets={
                'DB_PASSWORD': Secret.from_secrets_manager(
                    database.secret,
                    'password'
                ),
            },
            logging=LogDriver.aws_logs(
                stream_prefix='pyramid',
                mode=AwsLogDriverMode.NON_BLOCKING,
            ),
        )
        fargate_service.target_group.configure_health_check(
            interval=cdk.Duration.seconds(60),
        )
        cdk.Tags.of(fargate_service).add(
            'branch',
            branch
        )
        fargate_service.task_definition.task_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMManagedInstanceCore'
            )
        )
        cfn_service = fargate_service.service.node.default_child
        cfn_service.enable_execute_command = True
        scalable_task = fargate_service.service.auto_scale_task_count(
            max_capacity=4,
        )
        scalable_task.scale_on_request_count(
            'RequestCountScaling',
            requests_per_target=600,
            target_group=fargate_service.target_group,
            scale_in_cooldown=cdk.Duration.seconds(60),
            scale_out_cooldown=cdk.Duration.seconds(60),
        )
