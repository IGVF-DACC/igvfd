import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch import ComparisonOperator

from aws_cdk.aws_cloudwatch_actions import SnsAction

from aws_cdk.aws_opensearchservice import Domain

from infrastructure.constructs.existing.types import ExistingResources

from dataclasses import dataclass

from typing import Any
from typing import Union


CPU_ALARM_THRESHOLD_PERCENT = 85

JVM_MEMORY_THRESHOLD_PERCENT = 90

GIB_TO_MIB = 1024

PROPORTION_OF_FREE_STORAGE_THRESHOLD = 0.25

SEARCH_LATENCY_IN_MILLISECONDS_THRESHOLD = 1000


@dataclass
class OpensearchAlarmsProps:
    existing_resources: ExistingResources
    domain: Domain
    volume_size: int


class OpensearchAlarms(Construct):

    props: OpensearchAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: OpensearchAlarmsProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_alarm_action()
        self._add_cluster_status_red_alarm()
        self._add_cluster_blocking_writes_alarm()
        self._add_cpu_alarm()
        self._add_jvm_memory_alarm()
        self._add_storage_alarm()
        self._add_search_latency_alarm()

    def _define_alarm_action(self) -> None:
        # Cloudwatch action targeting SNS topic.
        self.alarm_action = SnsAction(
            self.props.existing_resources.notification.alarm_notification_topic
        )

    def _add_cluster_status_red_alarm(self) -> None:
        cluster_status_red_alarm = self.props.domain.metric_cluster_status_red().create_alarm(
            self,
            'ClusterStatusRedAlarm',
            evaluation_periods=1,
            threshold=1,
        )
        cluster_status_red_alarm.add_alarm_action(
            self.alarm_action
        )
        cluster_status_red_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_cluster_blocking_writes_alarm(self) -> None:
        cluster_blocking_writes_alarm = self.props.domain.metric_cluster_index_writes_blocked().create_alarm(
            self,
            'ClusterBlockingWritesAlarm',
            evaluation_periods=1,
            threshold=1,
        )
        cluster_blocking_writes_alarm.add_alarm_action(
            self.alarm_action
        )
        cluster_blocking_writes_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_cpu_alarm(self) -> None:
        cpu_alarm = self.props.domain.metric_cpu_utilization().create_alarm(
            self,
            'CPUAlarm',
            evaluation_periods=1,
            threshold=CPU_ALARM_THRESHOLD_PERCENT,
        )
        cpu_alarm.add_alarm_action(
            self.alarm_action
        )
        cpu_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_jvm_memory_alarm(self) -> None:
        jvm_memory_alarm = self.props.domain.metric_jvm_memory_pressure().create_alarm(
            self,
            'JVMMemoryAlarm',
            evaluation_periods=1,
            threshold=JVM_MEMORY_THRESHOLD_PERCENT,
        )
        jvm_memory_alarm.add_alarm_action(
            self.alarm_action
        )
        jvm_memory_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_storage_alarm(self) -> None:
        storage_alarm = self.props.domain.metric_free_storage_space().create_alarm(
            self,
            'StorageAlarm',
            evaluation_periods=1,
            threshold=int(self.props.volume_size * GIB_TO_MIB * PROPORTION_OF_FREE_STORAGE_THRESHOLD),
            comparison_operator=ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
        )
        storage_alarm.add_alarm_action(
            self.alarm_action
        )
        storage_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_search_latency_alarm(self) -> None:
        search_latency_alarm = self.props.domain.metric_search_latency().create_alarm(
            self,
            'SearchLatencyAlarm',
            evaluation_periods=1,
            threshold=SEARCH_LATENCY_IN_MILLISECONDS_THRESHOLD,
        )
        search_latency_alarm.add_alarm_action(
            self.alarm_action
        )
        search_latency_alarm.add_ok_action(
            self.alarm_action
        )
