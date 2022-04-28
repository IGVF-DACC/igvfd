import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion

from infrastructure.constructs.existing.types import ExistingResources

from typing import Any


class Postgres(Construct):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            branch: str,
            existing_resources: ExistingResources,
            allocated_storage: int,
            max_allocated_storage: int,
            instance_type: InstanceType,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._branch = branch
        self._existing_resources = existing_resources
        self._allocated_storage = allocated_storage
        self._max_allocated_storage = max_allocated_storage
        self._instance_type = instance_type
        self._define_engine()
        self._define_database_name()
        self._define_database()
        self._add_tags_to_database()

    def _define_engine(self) -> None:
        self.engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )

    def _define_database_name(self) -> None:
        self.database_name = 'igvfd'

    def _define_database(self) -> None:
        self.database = DatabaseInstance(
            self,
            'Postgres',
            database_name=self.database_name,
            engine=self.engine,
            instance_type=self._instance_type,
            vpc=self._existing_resources.network.vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
            allocated_storage=self._allocated_storage,
            max_allocated_storage=self._max_allocated_storage,
        )

    def _add_tags_to_database(self) -> None:
        cdk.Tags.of(self.database).add(
            'branch',
            self._branch
        )
