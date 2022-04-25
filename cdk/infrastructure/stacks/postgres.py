import aws_cdk as cdk

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion


class PostgresStack(cdk.Stack):

    def __init__(self, scope, construct_id, branch, existing_construct, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self._branch = branch
        self._existing_construct = existing_construct
        self._define_existing()
        self._define_engine()
        self._define_database_name()
        self._define_database()
        self._add_tags_to_database()

    def _define_existing(self):
        self._existing = self._existing_construct(
            self,
            'ExistingResources',
        )

    def _define_engine(self):
        self.engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )

    def _define_database_name(self):
        self.database_name = 'igvfd'

    def _define_database(self):
        self.database = DatabaseInstance(
            self,
            'Postgres',
            database_name=self.database_name,
            engine=self.engine,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
            vpc=self._existing.vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
            allocated_storage=10,
            max_allocated_storage=20,
        )

    def _add_tags_to_database(self):
        cdk.Tags.of(self.database).add(
            'branch',
            self._branch
        )
