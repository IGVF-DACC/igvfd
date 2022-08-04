import aws_cdk as cdk

from aws_cdk import Duration
from aws_cdk.aws_events_targets import EcsTask
from aws_cdk.aws_events_targets import ContainerOverride
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType
from aws_cdk.aws_events import Rule
from aws_cdk.aws_events import Schedule

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.backend import Backend
from infrastructure.constructs.backend import BackendProps

from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.constructs.postgres import PostgresConstruct

from typing import Any


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

        one_off_task_target = EcsTask(
            cluster=self.backend.fargate_service.cluster,
            task_definition=self.backend.fargate_service.task_definition,
            container_overrides=[
                ContainerOverride(
                    container_name='pyramid',
                    command=['echo', 'hello from pyramid one off task'],
                ),
                ContainerOverride(
                    container_name='nginx',
                    command=['sleep', '3600'],
                ),
            ],
            subnet_selection=SubnetSelection(
                subnet_type=SubnetType.PUBLIC
            )
        )

        Rule(
            self,
            'OneOffRule',
            schedule=Schedule.rate(
                Duration.minutes(1)
            ),
            targets=[one_off_task_target]
        )
