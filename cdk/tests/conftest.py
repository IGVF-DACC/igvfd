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
def existing_resources(mocker, domain, network, secret, chatbot, bus):
    mock = mocker.Mock()
    mock.domain = domain
    mock.network = network
    mock.docker_hub_credentials.secret = secret
    mock.code_star_connection.arn = 'some-code-star-arn'
    mock.notification.encode_dcc_chatbot = chatbot
    mock.bus = bus
    return mock


@pytest.fixture
def config(instance_type):
    from infrastructure.config import Config
    return Config(
        name='demo',
        branch='some-branch',
        pipeline='xyz',
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
        backend={
            'cpu': 1024,
            'memory_limit_mib': 2048,
            'desired_count': 1,
            'max_capacity': 4,
            'use_postgres_named': 'Postgres',
        },
        tags=[
            ('test', 'tag'),
        ]
    )
