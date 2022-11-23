import pytest


@pytest.fixture
def stack():
    from aws_cdk import Stack
    return Stack()


@pytest.fixture
def vpc(stack):
    from aws_cdk.aws_ec2 import SubnetConfiguration
    from aws_cdk.aws_ec2 import SubnetType
    from aws_cdk.aws_ec2 import Vpc
    vpc = Vpc(
        stack,
        'TestVpc',
        cidr='10.4.0.0/16',
        nat_gateways=0,
        subnet_configuration=[
            SubnetConfiguration(
                name='public',
                cidr_mask=20,
                subnet_type=SubnetType.PUBLIC,
            ),
            SubnetConfiguration(
                name='isolated',
                cidr_mask=20,
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
        ]
    )
    return vpc


@pytest.fixture
def instance_type():
    from aws_cdk.aws_ec2 import InstanceType
    from aws_cdk.aws_ec2 import InstanceClass
    from aws_cdk.aws_ec2 import InstanceSize
    return InstanceType.of(
        InstanceClass.BURSTABLE3,
        InstanceSize.MEDIUM,
    )


@pytest.fixture
def capacity_config():
    from aws_cdk.aws_opensearchservice import CapacityConfig
    return CapacityConfig(
        data_node_instance_type='t3.small.search',
        data_nodes=1,
    )


@pytest.fixture
def secret(stack):
    from aws_cdk.aws_secretsmanager import Secret
    return Secret(
        stack,
        'TestSecret',
    )


@pytest.fixture
def chatbot(stack):
    from aws_cdk.aws_chatbot import SlackChannelConfiguration
    return SlackChannelConfiguration(
        stack,
        'TestChatbot',
        slack_channel_configuration_name='some-config-name',
        slack_channel_id='some-channel-id',
        slack_workspace_id='some-workspace-id',
    )


@pytest.fixture
def sns_topic(stack):
    from aws_cdk.aws_sns import Topic
    return Topic(
        stack,
        'TestTopic',
    )


@pytest.fixture
def domain_name():
    return 'my.test.domain.org'


@pytest.fixture
def certificate(stack, domain_name):
    from aws_cdk.aws_certificatemanager import Certificate
    return Certificate(
        stack,
        'TestCertificate',
        domain_name=f'*.{domain_name}',
    )


@pytest.fixture
def hosted_zone(stack, domain_name):
    from aws_cdk.aws_route53 import HostedZone
    return HostedZone(
        stack,
        'TestHostedZone',
        zone_name=domain_name,
    )


@pytest.fixture
def network(mocker, vpc):
    mock = mocker.Mock()
    mock.vpc = vpc
    return mock


@pytest.fixture
def domain(mocker, domain_name, certificate, hosted_zone):
    mock = mocker.Mock()
    mock.name = domain_name
    mock.certificate = certificate
    mock.zone = hosted_zone
    return mock


@pytest.fixture
def event_bus(stack):
    from aws_cdk.aws_events import EventBus
    return EventBus(
        stack,
        'TestBus',
    )


@pytest.fixture
def bus(mocker, event_bus):
    mock = mocker.Mock()
    mock.default = event_bus
    return mock


@pytest.fixture
def existing_resources(mocker, domain, network, secret, chatbot, bus, sns_topic):
    mock = mocker.Mock()
    mock.domain = domain
    mock.network = network
    mock.docker_hub_credentials.secret = secret
    mock.portal_credentials.indexing_service_key = secret
    mock.code_star_connection.arn = 'some-code-star-arn'
    mock.notification.encode_dcc_chatbot = chatbot
    mock.notification.alarm_notification_topic = sns_topic
    mock.bus = bus
    return mock


@pytest.fixture
def pipeline_config():
    from infrastructure.config import PipelineConfig
    from infrastructure.constructs.existing import igvf_dev
    return PipelineConfig(
        name='demo',
        branch='some-branch',
        pipeline='xyz',
        existing_resources_class=igvf_dev.Resources,
        account_and_region=igvf_dev.US_WEST_2,
        tags=[
            ('test', 'tag'),
        ]
    )


@pytest.fixture
def config(instance_type, capacity_config):
    from infrastructure.config import Config
    return Config(
        name='demo',
        branch='some-branch',
        postgres={
            'instances': [
                {
                    'construct_id': 'Postgres',
                    'on': True,
                    'props': {
                        'allocated_storage': 10,
                        'max_allocated_storage': 20,
                        'instance_type': instance_type,
                    },
                },
            ],
        },
        opensearch={
            'capacity': capacity_config,
            'volume_size': 10,
        },
        backend={
            'cpu': 1024,
            'memory_limit_mib': 2048,
            'desired_count': 1,
            'max_capacity': 4,
            'use_postgres_named': 'Postgres',
        },
        invalidation_service={
            'cpu': 256,
            'memory_limit_mib': 512,
            'min_scaling_capacity': 1,
            'max_scaling_capacity': 2,
        },
        indexing_service={
            'cpu': 256,
            'memory_limit_mib': 512,
            'min_scaling_capacity': 1,
            'max_scaling_capacity': 2,
        },
        tags=[
            ('test', 'tag'),
        ]
    )


@pytest.fixture
def opensearch(stack, existing_resources, config):
    from infrastructure.constructs.opensearch import Opensearch
    from infrastructure.constructs.opensearch import OpensearchProps
    return Opensearch(
        stack,
        'Opensearch',
        props=OpensearchProps(
            **config.opensearch,
            config=config,
            existing_resources=existing_resources
        )
    )


@pytest.fixture
def transaction_queue(stack, existing_resources):
    from infrastructure.constructs.queue import QueueProps
    from infrastructure.constructs.queue import TransactionQueue
    return TransactionQueue(
        stack,
        'TransactionQueue',
        props=QueueProps(
            existing_resources=existing_resources,
        ),
    )


@pytest.fixture
def invalidation_queue(stack, existing_resources):
    from infrastructure.constructs.queue import QueueProps
    from infrastructure.constructs.queue import InvalidationQueue
    return InvalidationQueue(
        stack,
        'InvalidationQueue',
        props=QueueProps(
            existing_resources=existing_resources,
        ),
    )


@pytest.fixture
def application_load_balanced_fargate_service(stack, existing_resources):
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService
    from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
    return ApplicationLoadBalancedFargateService(
        stack,
        'TestApplicationLoadBalancedFargateService',
        vpc=existing_resources.network.vpc,
        assign_public_ip=True,
        task_image_options=ApplicationLoadBalancedTaskImageOptions(
            image=ContainerImage.from_registry('some-test-image')
        ),
    )


@pytest.fixture
def queue_processing_fargate_service(stack, existing_resources):
    from aws_cdk.aws_ecs import ContainerImage
    from aws_cdk.aws_ecs_patterns import QueueProcessingFargateService
    return QueueProcessingFargateService(
        stack,
        'QueueProcessingFargateService',
        vpc=existing_resources.network.vpc,
        assign_public_ip=True,
        image=ContainerImage.from_registry('some-test-image')
    )
