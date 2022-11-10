import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from aws_cdk.aws_cloudwatch import TreatMissingData

from aws_cdk.aws_cloudwatch_actions import SnsAction

from aws_cdk.aws_sqs import Queue

from infrastructure.constructs.existing.types import ExistingResources

from dataclasses import dataclass

from typing import Any


@dataclass
class QueueAlarmsProps:
    existing_resources: ExistingResources
    queue: Queue
    dead_letter_queue: Queue
    oldest_message_in_seconds_threshold: int


class QueueAlarms(Construct):

    props: QueueAlarmsProps
    alarm_action: SnsAction

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: QueueAlarmsProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_alarm_action()
        self._add_dead_letter_queue_has_messages_alarm()

    def _define_alarm_action(self) -> None:
        # Cloudwatch action targeting SNS topic.
        self.alarm_action = SnsAction(
            self.props.existing_resources.notification.alarm_notification_topic
        )

    def _add_dead_letter_queue_has_messages_alarm(self) -> None:
        dlq_has_messages_alarm = self.props.dead_letter_queue.metric_approximate_number_of_messages_visible().create_alarm(
            self,
            'DeadLetterQueueHasMessagesAlarm',
            evaluation_periods=1,
            threshold=1,
        )
        dlq_has_messages_alarm.add_alarm_action(
            self.alarm_action
        )
        dlq_has_messages_alarm.add_ok_action(
            self.alarm_action
        )

    def _add_queue_has_old_messages_alarm(self) -> None:
        queue_has_old_messages_alarm = self.props.queue.metric_approximate_age_of_oldest_message().create_alarm(
            self,
            'QueueHasOldMessagesAlarm',
            evaluation_periods=1,
            threshold=self.props.oldest_message_in_seconds_threshold,
        )
        queue_has_old_messages_alarm.add_alarm_action(
            self.alarm_action
        )
        queue_has_old_messages_alarm.add_ok_action(
            self.alarm_action
        )
