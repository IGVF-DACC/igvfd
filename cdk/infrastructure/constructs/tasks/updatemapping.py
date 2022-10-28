import json

from constructs import Construct

from aws_cdk.aws_logs import RetentionDays

from aws_cdk.custom_resources import AwsCustomResource
from aws_cdk.custom_resources import AwsCustomResourcePolicy
from aws_cdk.custom_resources import AwsSdkCall
from aws_cdk.custom_resources import PhysicalResourceId

from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService

from aws_cdk.aws_events import Rule
from aws_cdk.aws_events import EventPattern

from aws_cdk.aws_events_targets import ContainerOverride
from aws_cdk.aws_events_targets import EcsTask

from aws_cdk.aws_s3_assets import Asset

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources

from infrastructure.events.naming import get_event_source_from_config

from infrastructure.events.batchupgrade import BatchUpgradeEvents

from dataclasses import dataclass

from typing import Any
from typing import List


@dataclass
class UpdateMappingProps:
    config: Config
    existing_resources: ExistingResources
    fargate_service: ApplicationLoadBalancedFargateService


class UpdateMapping(Construct):

    event_source: str
    event_detail_type: str
    event_target: EcsTask
    event_rule: Rule
    event_trigger: AwsCustomResource
    upgrade_folder: Asset

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: UpdateMappingProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_event_source()
        self._define_event_detail_type()
        self._define_event_target()
        self._define_event_rule()
        self._define_upgrade_folder()
        self._define_event_trigger()
        self._ensure_rule_exists_before_trigger()

    def _define_event_source(self) -> None:
        self.event_source = get_event_source_from_config(
            self.props.config
        )

    def _define_event_detail_type(self) -> None:
        self.event_detail_type = BatchUpgradeEvents.UPGRADE_FOLDER_CHANGED

    def _get_container_overrides(self) -> List[ContainerOverride]:
        return [
            ContainerOverride(
                container_name='pyramid',
                command=['/scripts/pyramid/delete-and-create-mapping-and-reindex.sh'],
            ),
            ContainerOverride(
                container_name='nginx',
                command=['sleep', '3600'],
            ),
        ]

    def _get_subnet_selection(self) -> SubnetSelection:
        return SubnetSelection(
            subnet_type=SubnetType.PUBLIC
        )

    def _define_event_target(self) -> None:
        self.event_target = EcsTask(
            cluster=self.props.fargate_service.cluster,
            task_definition=self.props.fargate_service.task_definition,
            container_overrides=self._get_container_overrides(),
            security_groups=self.props.fargate_service.service.connections.security_groups,
            subnet_selection=self._get_subnet_selection(),
        )

    def _define_event_rule(self) -> None:
        self.event_rule = Rule(
            self,
            'RunUpdateMapping',
            event_pattern=EventPattern(
                detail_type=[
                    self.event_detail_type,
                ],
                source=[
                    self.event_source,
                ],
            ),
            targets=[
                self.event_target,
            ]
        )

    def _define_upgrade_folder(self) -> None:
        self.upgrade_folder = Asset(
            self,
            'UpgradeFolder',
            path='../src/igvfd/upgrade',
        )

    def _define_event_trigger(self) -> None:
        # Put UpgradeFolderChanged event onto EventBridge bus
        # when the upgrade folder asset hash changes.
        self.event_trigger = AwsCustomResource(
            self,
            'PutUpgradeFolderChangedEvent',
            on_update=AwsSdkCall(
                service='EventBridge',
                action='putEvents',
                parameters={
                    'Entries': [
                        {
                            'DetailType': self.event_detail_type,
                            'Source': self.event_source,
                            'Detail': json.dumps({}),
                        }
                    ]
                },
                physical_resource_id=PhysicalResourceId.of(
                    self.upgrade_folder.asset_hash
                )
            ),
            log_retention=RetentionDays.ONE_DAY,
            policy=AwsCustomResourcePolicy.from_sdk_calls(
                resources=[
                    self.props.existing_resources.bus.default.event_bus_arn,
                ]
            ),
        )

    def _grant_put_events_to_trigger(self) -> None:
        self.props.existing_resources.bus.default.grant_put_events_to(
            self.event_trigger
        )

    def _ensure_rule_exists_before_trigger(self) -> None:
        self.event_trigger.node.add_dependency(
            self.event_rule
        )
