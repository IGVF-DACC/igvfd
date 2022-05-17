import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceFromSnapshot
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion
from aws_cdk.aws_rds import SnapshotCredentials

from dataclasses import dataclass

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.snapshot import LatestSnapshotFromDB

from typing import Any
from typing import Type


@dataclass
class PostgresProps:
    config: Config
    existing_resources: ExistingResources
    allocated_storage: int
    max_allocated_storage: int
    instance_type: InstanceType


class PostgresBase(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: PostgresProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_engine()
        self._define_database_name()

    def _define_engine(self) -> None:
        self.engine = DatabaseInstanceEngine.postgres(
            version=PostgresEngineVersion.VER_14_1
        )

    def _define_database_name(self) -> None:
        self.database_name = 'igvfd'

    def _add_tags_to_database(self) -> None:
        cdk.Tags.of(self.database).add(
            'branch',
            self.props.config.branch,
        )


class Postgres(PostgresBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: PostgresProps,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )
        self._define_database()
        self._add_tags_to_database()

    def _define_database(self) -> None:
        self.database = DatabaseInstance(
            self,
            'Postgres',
            database_name=self.database_name,
            engine=self.engine,
            instance_type=self.props.instance_type,
            vpc=self.props.existing_resources.network.vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
            allocated_storage=self.props.allocated_storage,
            max_allocated_storage=self.props.max_allocated_storage,
        )


class PostgresFromSnapshot(PostgresBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: PostgresProps,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )
        self._get_latest_snapshot_id()
        self._define_database()
        self._add_tags_to_database()

    def _get_latest_snapshot_id(self) -> None:
        self._latest_snapshot = LatestSnapshotFromDB(
            self,
            'LatestSnapshotFromDB',
            db_instance_identifier=self.props.config.snapshot_source_db_identifier
        )

    def _define_database(self) -> None:
        self.database = DatabaseInstanceFromSnapshot(
            self,
            'PostgresFromSnapshot',
            snapshot_identifier=self._latest_snapshot.arn,
            credentials=SnapshotCredentials.from_generated_secret(
                'postgres',
            ),
            database_name=self.database_name,
            engine=self.engine,
            instance_type=self.props.instance_type,
            vpc=self.props.existing_resources.network.vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
            allocated_storage=self.props.allocated_storage,
            max_allocated_storage=self.props.max_allocated_storage,
        )


def postgres_factory(config: Config) -> Type[Postgres]:
    if config.snapshot_source_db_identifier is not None:
        return PostgresFromSnapshot
    return Postgres
