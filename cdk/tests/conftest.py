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
