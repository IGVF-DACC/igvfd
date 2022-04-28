import aws_cdk as cdk

from infrastructure.constructs.postgres import Postgres

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize


class PostgresStack(cdk.Stack):

    def __init__(self, scope, construct_id, *, branch, existing_resources, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources(
            self,
            'ExistingResources',
        )
        self.postgres = Postgres(
            self,
            'Postgres',
            branch=branch,
            existing_resources=self.existing_resources,
            allocated_storage=10,
            max_allocated_storage=20,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
        )
