import aws_cdk as cdk

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion

from infrastructure.constructs.existing import ExistingResources


class PostgresStack(cdk.Stack):

    def __init__(self, scope, construct_id, branch, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        existing = ExistingResources(
            self,
            'ExistingResources',
        )
        self.engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )
        self.database_name = 'igvfd'
        self.database = DatabaseInstance(
            self,
            'Postgres',
            database_name=self.database_name,
            engine=self.engine,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
            vpc=existing.vpcs.default_vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PUBLIC,
            ),
            allocated_storage=10,
            max_allocated_storage=20,
            security_groups=[
                existing.security_groups.encd_demos,
            ],
        )
