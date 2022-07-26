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


from aws_cdk.aws_cloudwatch import Alarm
from aws_cdk.aws_cloudwatch_actions import SnsAction


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


class PostgresFromSnapshot(PostgresBase):

    database: DatabaseInstanceFromSnapshot
    latest_snapshot: LatestSnapshotFromDB
    db_instance_identifier: str

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
        self._add_metric_alarms()

    def _get_latest_snapshot_id(self) -> None:
        # Make mypy happy. The factory already
        # checks that this is not None.
        self.db_instance_identifier = cast(
            str,
            self.props.config.snapshot_source_db_identifier
        )
        self.latest_snapshot = LatestSnapshotFromDB(
            self,
            'LatestSnapshotFromDB',
            db_instance_identifier=self.db_instance_identifier
        )

    def _define_database(self) -> None:
        self.database = DatabaseInstanceFromSnapshot(
            self,
            'PostgresFromSnapshot',
            snapshot_identifier=self.latest_snapshot.arn,
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
            'snapshot_source_db_identifier',
            self.db_instance_identifier
        )
        tags.add(
            'from_snapshot_arn',
            self.latest_snapshot.arn,
        )

    def _add_metric_alarms(self) -> None:
        events_topic_action = SnsAction(
            self.props.existing_resources.events_topic
        )
        cpu_alarm = self.database.metric_cpu_utilization().create_alarm(
            self,
            'PostgresCPUUtilizationAlarm',
            evaluation_periods=1,
            threshold=0.50,
        )
        cpu_alarm.add_alarm_action(
            events_topic_action,
        )
        cpu_alarm.add_ok_action(
            events_topic_action,
        )
        storage_alarm = self.database.metric_free_storage_space().create_alarm(
            self,
            'PostgresStorageAlarm',
            evaluation_periods=1,
            threshold=self.props.allocated_storage // 2,
        )
        storage_alarm.add_alarm_action(
            events_topic_action
        )
        storage_alarm.add_ok_action(
            events_topic_action
        )


PostgresConstruct = Union[Postgres, PostgresFromSnapshot]

PostgresConstructClass = Union[Type[Postgres], Type[PostgresFromSnapshot]]


def postgres_factory(config: Config) -> PostgresConstructClass:
    if config.snapshot_source_db_identifier is not None:
        return PostgresFromSnapshot
    return Postgres
