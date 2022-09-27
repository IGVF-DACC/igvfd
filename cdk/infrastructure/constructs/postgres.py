from aws_cdk import Stack
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

from infrastructure.constructs.alarms.postgres import PostgresAlarmsProps
from infrastructure.constructs.alarms.postgres import PostgresAlarms

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.snapshot import LatestSnapshotFromDB

from typing import Any
from typing import cast
from typing import Type
from typing import Union
from typing import Optional

from dataclasses import dataclass


@dataclass
class PostgresProps:
    config: Config
    existing_resources: ExistingResources
    allocated_storage: int
    max_allocated_storage: int
    instance_type: InstanceType
    auto_minor_version_upgrade: bool = False
    snapshot_arn: Optional[str] = None
    snapshot_source_db_identifier: Optional[str] = None


class PostgresBase(Construct):

    database_name: str
    engine: IInstanceEngine
    props: PostgresProps
    database: Union[DatabaseInstance, DatabaseInstanceFromSnapshot]

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
            version=PostgresEngineVersion.VER_14_3
        )

    def _define_database_name(self) -> None:
        self.database_name = 'igvfd'

    def _export_values(self) -> None:
        raise NotImplementedError

    def _add_alarms(self) -> None:
        PostgresAlarms(
            self,
            'PostgresAlarms',
            props=PostgresAlarmsProps(
                config=self.props.config,
                existing_resources=self.props.existing_resources,
                database=self.database,
            )
        )

    def _post_init(self) -> None:
        self._add_alarms()
        self._export_values()


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
        self._post_init()

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
            auto_minor_version_upgrade=self.props.auto_minor_version_upgrade,
        )

    def _add_tags_to_database(self) -> None:
        Tags.of(self.database).add(
            'branch',
            self.props.config.branch,
        )

    def _export_values(self) -> None:
        export_default_explicit_values(self)


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
        self._post_init()

    def _get_snapshot_arn(self) -> str:
        return cast(
            str,
            self.props.snapshot_arn,
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
            auto_minor_version_upgrade=self.props.auto_minor_version_upgrade,
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

    def _export_values(self) -> None:
        export_default_explicit_values(self)


class PostgresFromLatestSnapshot(PostgresFromSnapshotArn):

    database: DatabaseInstanceFromSnapshot
    latest_snapshot: LatestSnapshotFromDB
    db_instance_identifier: str

    def _build(self) -> None:
        self._define_latest_snapshot()
        self._define_database()
        self._add_tags_to_database()
        self._post_init()

    def _get_db_instance_identifier(self) -> str:
        # Make mypy happy. The factory already
        # checks that this is not None.
        return cast(
            str,
            self.props.snapshot_source_db_identifier
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

    def _export_values(self) -> None:
        export_default_explicit_values(self)


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


def postgres_factory(props: PostgresProps) -> PostgresConstructClass:
    if props.snapshot_arn is not None:
        return PostgresFromSnapshotArn
    elif props.snapshot_source_db_identifier is not None:
        return PostgresFromLatestSnapshot
    return Postgres


def export_default_explicit_values(postgres: PostgresConstruct) -> None:
    parent_stack = Stack.of(postgres)
    parent_stack.export_value(
        postgres.database.instance_endpoint.hostname
    )
    if postgres.database.secret is not None:
        parent_stack.export_value(
            postgres.database.secret.secret_full_arn
        )
    for security_group in postgres.database.connections.security_groups:
        parent_stack.export_value(
            security_group.security_group_id
        )
