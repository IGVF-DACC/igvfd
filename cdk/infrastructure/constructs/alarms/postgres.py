import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch_actions import SnsAction

from aws_cdk.aws_rds import DatabaseInstance
from aws_cdk.aws_rds import DatabaseInstanceFromSnapshot

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources

from dataclasses import dataclass

from typing import Any
from typing import Union


CPU_ALARM_THRESHOLD_PERCENT = 85

STORAGE_ALARM_THRESHOLD_PERCENT = 80


@dataclass
class PostgresAlarmsProps:
    config: Config
    existing_resources: ExistingResources
    database: Union[DatabaseInstance, DatabaseInstanceFromSnapshot]
    allocated_storage: int


class PostgresAlarms(Construct):

    props: PostgresAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: PostgresAlarmsProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_alarm_action()
        self._add_cpu_alarm()
        self._add_storage_alarm()

    def _define_alarm_action(self) -> None:
        # Cloudwatch action targeting SNS topic.
        self.alarm_action = SnsAction(
            self.props.existing_resources.notification.alarm_notification_topic
        )

    def _add_cpu_alarm(self) -> None:
        cpu_alarm = self.props.database.metric_cpu_utilization().create_alarm(
            self,
            'PostgresCPUUtilizationAlarm',
            evaluation_periods=1,
            threshold=CPU_ALARM_THRESHOLD_PERCENT,
        )
        cpu_alarm.add_alarm_action(
            self.alarm_action
        )
        cpu_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_storage_alarm(self) -> None:
        storage_alarm = self.props.database.metric_free_storage_space().create_alarm(
            self,
            'PostgresStorageAlarm',
            evaluation_periods=1,
            threshold=int(
                self.props.allocated_storage * (
                    STORAGE_ALARM_THRESHOLD_PERCENT * 0.01
                )
            )
        )
        storage_alarm.add_alarm_action(
            self.alarm_action
        )
        storage_alarm.add_ok_action(
            self.alarm_action
        )
