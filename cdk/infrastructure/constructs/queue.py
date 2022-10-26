from aws_cdk import Duration

from constructs import Construct

from aws_cdk.aws_sqs import DeadLetterQueue
from aws_cdk.aws_sqs import Queue

from typing import Any


class QueueBase(Construct):

    dead_letter_queue: Queue
    queue: Queue

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._define_dead_letter_queue()
        self._define_queue()

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


class TransactionQueue(QueueBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )


class InvalidationQueue(QueueBase):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs: Any
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )
