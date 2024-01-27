from aws_cdk import Duration

from constructs import Construct

from aws_cdk.aws_sqs import DeadLetterQueue
from aws_cdk.aws_sqs import Queue

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.alarms.queue import QueueAlarmsProps
from infrastructure.constructs.alarms.queue import QueueAlarms

from dataclasses import dataclass

from typing import Any


@dataclass
class QueueProps:
    existing_resources: ExistingResources


class QueueBase(Construct):

    props: QueueProps
    dead_letter_queue: Queue
    queue: Queue

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: QueueProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_dead_letter_queue()
        self._define_queue()
        self._add_alarms()

    def _define_dead_letter_queue(self) -> None:
        self.dead_letter_queue = Queue(
            self,
            'DeadLetterQueue',
            retention_period=Duration.days(14),
        )

    def _define_queue(self) -> None:
        self.queue = Queue(
            self,
            'Queue',
            visibility_timeout=Duration.seconds(120),
            dead_letter_queue=DeadLetterQueue(
                queue=self.dead_letter_queue,
                max_receive_count=3,
            )
        )

    def _add_alarms(self) -> None:
        pass


class TransactionQueue(QueueBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: QueueProps,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )

    def _add_alarms(self) -> None:
        QueueAlarms(
            self,
            'TransactionQueueAlarms',
            props=QueueAlarmsProps(
                existing_resources=self.props.existing_resources,
                queue=self.queue,
                dead_letter_queue=self.dead_letter_queue,
                oldest_message_in_seconds_threshold=3600,
            ),
        )


class InvalidationQueue(QueueBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: QueueProps,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )

    def _add_alarms(self) -> None:
        QueueAlarms(
            self,
            'InvalidationQueueAlarms',
            props=QueueAlarmsProps(
                existing_resources=self.props.existing_resources,
                queue=self.queue,
                dead_letter_queue=self.dead_letter_queue,
                oldest_message_in_seconds_threshold=86400,
            ),
        )
