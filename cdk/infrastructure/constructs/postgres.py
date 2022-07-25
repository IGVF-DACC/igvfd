from aws_cdk import Tags

from constructs import Construct

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceFromSnapshot
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import IInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion
from aws_cdk.aws_rds import SnapshotCredentials

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.snapshot import LatestSnapshotFromDB

from typing import Any
from typing import cast
from typing import Type
from typing import Union

from dataclasses import dataclass


@dataclass
class PostgresProps:
    config: Config
    existing_resources: ExistingResources
    allocated_storage: int
    max_allocated_storage: int
    instance_type: InstanceType


class PostgresBase(Construct):

    database_name: str
    engine: IInstanceEngine
    props: PostgresProps

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


class Postgres(PostgresBase):

    database: DatabaseInstance

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
        self._build()

    def _build(self) -> None:
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

    def _add_tags_to_database(self) -> None:
        Tags.of(self.database).add(
            'branch',
            self.props.config.branch,
        )


class PostgresFromSnapshotArn(PostgresBase):

    database: DatabaseInstanceFromSnapshot

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
        self._build()

    def _build(self) -> None:
        self._define_database()
        self._add_tags_to_database()

    def _get_snapshot_arn(self) -> str:
        return cast(
            str,
            self.props.config.snapshot_arn,
        )

    def _define_database(self) -> None:
        self.database = DatabaseInstanceFromSnapshot(
            self,
            'PostgresFromSnapshot',
            snapshot_identifier=self._get_snapshot_arn(),
            credentials=SnapshotCredentials.from_generated_secret(
                'postgres',
            ),
            engine=self.engine,
            instance_type=self.props.instance_type,
            vpc=self.props.existing_resources.network.vpc,
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PRIVATE_ISOLATED,
            ),
            allocated_storage=self.props.allocated_storage,
            max_allocated_storage=self.props.max_allocated_storage,
        )

    def _add_tags_to_database(self) -> None:
        tags = Tags.of(self.database)
        tags.add(
            'branch',
            self.props.config.branch,
        )
        tags.add(
            'snapshot_arn',
            self._get_snapshot_arn(),
        )


class PostgresFromLatestSnapshot(PostgresFromSnapshotArn):

    database: DatabaseInstanceFromSnapshot
    latest_snapshot: LatestSnapshotFromDB
    db_instance_identifier: str

    def _build(self) -> None:
        self._define_latest_snapshot()
        self._define_database()
        self._add_tags_to_database()

    def _get_db_instance_identifier(self) -> str:
        # Make mypy happy. The factory already
        # checks that this is not None.
        return cast(
            str,
            self.props.config.snapshot_source_db_identifier
        )

    def _define_latest_snapshot(self) -> None:
        self.latest_snapshot = LatestSnapshotFromDB(
            self,
            'LatestSnapshotFromDB',
            db_instance_identifier=self._get_db_instance_identifier(),
        )

    def _get_snapshot_arn(self) -> str:
        return self.latest_snapshot.arn

    def _add_tags_to_database(self) -> None:
        tags = Tags.of(self.database)
        tags.add(
            'branch',
            self.props.config.branch,
        )
        tags.add(
            'snapshot_source_db_identifier',
            self._get_db_instance_identifier(),
        )
        tags.add(
            'latest_snapshot_arn',
            self.latest_snapshot.arn,
        )


PostgresConstruct = Union[
    Postgres,
    PostgresFromSnapshotArn,
    PostgresFromLatestSnapshot
]

PostgresConstructClass = Union[
    Type[Postgres],
    Type[PostgresFromSnapshotArn],
    Type[PostgresFromLatestSnapshot]
]


def postgres_factory(config: Config) -> PostgresConstructClass:
    if config.snapshot_arn is not None:
        return PostgresFromSnapshotArn
    elif config.snapshot_source_db_identifier is not None:
        return PostgresFromLatestSnapshot
    return Postgres
