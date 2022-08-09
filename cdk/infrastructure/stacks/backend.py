import aws_cdk as cdk

from aws_cdk import Duration

from aws_cdk.aws_events_targets import EcsTask
from aws_cdk.aws_events_targets import ContainerOverride

from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType
from aws_cdk.aws_ec2 import Port

from aws_cdk.aws_events import EventBus
from aws_cdk.aws_events import Rule
from aws_cdk.aws_events import Schedule
from aws_cdk.aws_events import EventPattern

from aws_cdk.aws_s3_assets import Asset

from aws_cdk.custom_resources import AwsCustomResource
from aws_cdk.custom_resources import AwsCustomResourcePolicy
from aws_cdk.custom_resources import AwsSdkCall
from aws_cdk.custom_resources import PhysicalResourceId

from aws_cdk.aws_logs import RetentionDays

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.backend import BackendProps

from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.constructs.postgres import PostgresConstruct

from typing import Any
from typing import Dict

from dataclasses import dataclass


@dataclass
class EventDetails:
    metadata: Dict[str, Any]
    data: Dict[str, Any]


@dataclass
class Event:
    details: EventDetails
    detail_type: str
    source: str


event = Event(
    source='pyramid-application-branch-123',
    detail_type='RunTask',
    details=EventDetails(
        metadata={
            'some': 'extra info',
        },
        data={
            'payload': 'data'
        }
    )
)


class BackendStack(cdk.Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            postgres: PostgresConstruct,
            existing_resources_class: ExistingResourcesClass,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.backend = Backend(
            self,
            'Backend',
            props=BackendProps(
                config=config,
                existing_resources=self.existing_resources,
                postgres=postgres,
                cpu=1024,
                memory_limit_mib=2048,
                desired_count=1,
                max_capacity=4,
            )
        )

        batch_upgrade_task_target = EcsTask(
            cluster=self.backend.fargate_service.cluster,
            task_definition=self.backend.fargate_service.task_definition,
            container_overrides=[
                ContainerOverride(
                    container_name='pyramid',
                    command=['/scripts/pyramid/batchupgrade.sh'],
                ),
                ContainerOverride(
                    container_name='nginx',
                    command=['sleep', '3600'],
                ),
            ],
            subnet_selection=SubnetSelection(
                subnet_type=SubnetType.PUBLIC
            ),
        )

        if batch_upgrade_task_target.security_groups is not None:
            for security_group in batch_upgrade_task_target.security_groups:
                security_group.connections.allow_to(
                    postgres.database,
                    Port.tcp(5432),
                    description='Allow connection to Postgres instance',
                )

        EVENT_SOURCE = f'{config.common.project_name}.{config.name}.{config.branch}'

        RUN_BATCH_UPGRADE_EVENT = 'RunBatchUpgrade'

        Rule(
            self,
            'OneOffRule',
            event_pattern=EventPattern(
                detail_type=[
                    RUN_BATCH_UPGRADE_EVENT,
                ],
                source=[
                    EVENT_SOURCE,
                ],
            ),
            targets=[
                batch_upgrade_task_target,
            ]
        )

        upgrade_folder = Asset(
            self,
            'UpgradeFolder',
            path='../src/igvfd/upgrade',
        )

        event_bus = EventBus.from_event_bus_arn(
            self,
            'DefaultBus',
            'arn:aws:events:us-west-2:109189702753:event-bus/default'
        )

        trigger_batch_upgrade = AwsCustomResource(
            self,
            'TriggerBatchUpgrade',
            on_update=AwsSdkCall(
                service='EventBridge',
                action='putEvents',
                parameters={
                    'Entries': [
                        {
                            'DetailType': RUN_BATCH_UPGRADE_EVENT,
                            'Source': EVENT_SOURCE,
                        }
                    ]
                },
                physical_resource_id=PhysicalResourceId.of(
                    upgrade_folder.asset_hash
                )
            ),
            log_retention=RetentionDays.ONE_DAY,
            policy=AwsCustomResourcePolicy.from_sdk_calls(
                resources=[
                    event_bus.event_bus_arn,
                ]
            ),
        )

        event_bus.grant_put_events_to(trigger_batch_upgrade)
