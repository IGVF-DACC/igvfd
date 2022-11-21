import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch_actions import SnsAction

from aws_cdk.aws_ecs_patterns import QueueProcessingFargateService

from infrastructure.constructs.existing.types import ExistingResources

from dataclasses import dataclass

from typing import Any


CPU_ALARM_THRESHOLD_PERCENT = 85

MEMORY_ALARM_THRESHOLD_PERCENT = 80


@dataclass
class InvalidationServiceAlarmsProps:
    existing_resources: ExistingResources
    fargate_service: QueueProcessingFargateService


class InvalidationServiceAlarms(Construct):

    props: InvalidationServiceAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: InvalidationServiceAlarmsProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_alarm_action()
        self._add_cpu_alarm()
        self._add_memory_alarm()

    def _define_alarm_action(self) -> None:
        # Cloudwatch action targeting SNS topic.
        self.alarm_action = SnsAction(
            self.props.existing_resources.notification.alarm_notification_topic
        )

    def _add_cpu_alarm(self) -> None:
        cpu_alarm = self.props.fargate_service.service.metric_cpu_utilization().create_alarm(
            self,
            'CPUAlarm',
            evaluation_periods=2,
            threshold=CPU_ALARM_THRESHOLD_PERCENT,
        )
        cpu_alarm.add_alarm_action(
            self.alarm_action
        )
        cpu_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_memory_alarm(self) -> None:
        memory_alarm = self.props.fargate_service.service.metric_memory_utilization().create_alarm(
            self,
            'MemoryAlarm',
            evaluation_periods=1,
            threshold=MEMORY_ALARM_THRESHOLD_PERCENT,
        )
        memory_alarm.add_alarm_action(
            self.alarm_action
        )
        memory_alarm.add_ok_action(
            self.alarm_action
        )


@dataclass
class IndexingServiceAlarmsProps:
    existing_resources: ExistingResources
    fargate_service: QueueProcessingFargateService


class IndexingServiceAlarms(Construct):

    props: IndexingServiceAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: IndexingServiceAlarmsProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_alarm_action()
        self._add_cpu_alarm()
        self._add_memory_alarm()

    def _define_alarm_action(self) -> None:
        # Cloudwatch action targeting SNS topic.
        self.alarm_action = SnsAction(
            self.props.existing_resources.notification.alarm_notification_topic
        )

    def _add_cpu_alarm(self) -> None:
        cpu_alarm = self.props.fargate_service.service.metric_cpu_utilization().create_alarm(
            self,
            'CPUAlarm',
            evaluation_periods=2,
            threshold=CPU_ALARM_THRESHOLD_PERCENT,
        )
        cpu_alarm.add_alarm_action(
            self.alarm_action
        )
        cpu_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_memory_alarm(self) -> None:
        memory_alarm = self.props.fargate_service.service.metric_memory_utilization().create_alarm(
            self,
            'MemoryAlarm',
            evaluation_periods=1,
            threshold=MEMORY_ALARM_THRESHOLD_PERCENT,
        )
        memory_alarm.add_alarm_action(
            self.alarm_action
        )
        memory_alarm.add_ok_action(
            self.alarm_action
        )
