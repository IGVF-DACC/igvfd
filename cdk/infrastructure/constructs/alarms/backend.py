import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from aws_cdk.aws_cloudwatch_actions import SnsAction

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService

from infrastructure.constructs.existing.types import ExistingResources

from dataclasses import dataclass

from typing import Any


@dataclass
class BackendAlarmsProps:
    config: Config
    existing_resources: ExistingResources
    fargate_service: ApplicationLoadBalancedFargateService


class BackendAlarms(Construct):

    props: BackendAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: BackendAlarmsProps,
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
            'FargateServiceCPUAlarm',
            evaluation_periods=2,
            threshold=85,
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
            'FargateServiceMemoryAlarm',
            evaluation_periods=1,
            threshold=90,
        )
        memory_alarm.add_alarm_action(
            self.alarm_action
        )
        memory_alarm.add_ok_action(
            self.alarm_action
        )
