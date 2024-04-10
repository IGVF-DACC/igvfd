from constructs import Construct

from aws_cdk import Duration

from aws_cdk.aws_applicationautoscaling import Schedule

from aws_cdk.aws_ecs import AwsLogDriverMode
from aws_cdk.aws_ecs import LogDriver
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs import ICluster

from aws_cdk.aws_ecs_patterns import ScheduledFargateTask
from aws_cdk.aws_ecs_patterns import ScheduledFargateTaskImageOptions

from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_events import Rule
from aws_cdk.aws_events import EventPattern

from aws_cdk.aws_logs import RetentionDays

from infrastructure.config import Config

from infrastructure.events.naming import get_event_source_from_config

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.constructs.queue import InvalidationQueue

from typing import Any

from dataclasses import dataclass


@dataclass
class DeduplicateInvalidationQueueProps:
    config: Config
    existing_resources: ExistingResources
    cluster: ICluster
    invalidation_queue: InvalidationQueue
    number_of_workers: int
    minutes_to_wait_between_runs: int
    cpu: int
    memory_limit_mib: int


class DeduplicateInvalidationQueue(Construct):

    event_source: str
    event_detail_type: str
    event_rule: Rule
    application_image: ContainerImage
    scheduled_fargate_task: ScheduledFargateTask

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: DeduplicateInvalidationQueueProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_event_source()
        self._define_event_detail_type()
        self._define_docker_asset()
        self._define_log_driver_for_application_container()
        self._define_scheduled_fargate_task()
        self._allow_task_to_read_and_write_from_invalidation_queue()
        self._define_manual_event_rule()

    def _define_event_source(self) -> None:
        self.event_source = get_event_source_from_config(
            self.props.config
        )

    def _define_event_detail_type(self) -> None:
        self.event_detail_type = 'DeduplicateInvalidationQueue'

    def _define_docker_asset(self) -> None:
        self.application_image = ContainerImage.from_asset(
            '../',
            file='docker/dedup/Dockerfile',
        )

    def _define_log_driver_for_application_container(self) -> None:
        self.application_log_driver = LogDriver.aws_logs(
            stream_prefix='deduplicator',
            mode=AwsLogDriverMode.NON_BLOCKING,
            log_retention=RetentionDays.ONE_MONTH,
        )

    def _define_scheduled_fargate_task(self) -> None:
        self.scheduled_fargate_task = ScheduledFargateTask(
            self,
            'ScheduledFargateTask',
            scheduled_fargate_task_image_options=ScheduledFargateTaskImageOptions(
                image=self.application_image,
                environment={
                    'QUEUE_URL': self.props.invalidation_queue.queue.queue_url,
                    'NUM_WORKERS': f'{self.props.number_of_workers}',
                },
                log_driver=self.application_log_driver,
                cpu=self.props.cpu,
                memory_limit_mib=self.props.memory_limit_mib,
            ),
            schedule=Schedule.rate(
                Duration.minutes(
                    self.props.minutes_to_wait_between_runs
                )
            ),
            cluster=self.props.cluster,
            subnet_selection=SubnetSelection(
                subnet_type=SubnetType.PUBLIC
            ),
        )

    def _allow_task_to_read_and_write_from_invalidation_queue(self) -> None:
        self.props.invalidation_queue.queue.grant_send_messages(
            self.scheduled_fargate_task.task_definition.task_role
        )

    def _define_manual_event_rule(self) -> None:
        self.event_rule = Rule(
            self,
            'RunDeduplicateInvalidationQueue',
            event_pattern=EventPattern(
                detail_type=[
                    self.event_detail_type,
                ],
                source=[
                    self.event_source,
                ],
            ),
            targets=[
                self.scheduled_fargate_task.task,
            ]
        )
