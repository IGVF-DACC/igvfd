import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize

from infrastructure.constructs.existing.types import ExistingResourcesClass
from infrastructure.constructs.postgres import Postgres

from typing import Any


class PostgresStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            existing_resources_class: ExistingResourcesClass,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources_class(
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
