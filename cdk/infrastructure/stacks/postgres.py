import aws_cdk as cdk

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.existing.types import ExistingResources
from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.constructs.postgres import PostgresProps
from infrastructure.constructs.postgres import PostgresConstructClass
from infrastructure.constructs.postgres import postgres_factory

from infrastructure.multiplexer import MultiplexerConfig
from infrastructure.multiplexer import Multiplexer

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dataclasses import dataclass
from dataclasses import field


@dataclass
class PostgresConfig:
    construct_id: str
    on: bool
    props: Dict[str, Any]


def map_postgres_to_multiplexer_config(
        postgres_config: PostgresConfig,
        postgres_props: PostgresProps,
        postgres_class: PostgresConstructClass,
) -> MultiplexerConfig:
    return MultiplexerConfig(
        construct_id=postgres_config.construct_id,
        on=postgres_config.on,
        construct_class=postgres_class,
        kwargs={
            'props': postgres_props
        },
    )


class PostgresStack(cdk.Stack):

    multiplexer: Multiplexer

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            config: Config,
            existing_resources_class: ExistingResourcesClass,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.config = config
        self.existing_resources_class = existing_resources_class
        self.kwargs = kwargs
        self.multiplexer_configs: List[MultiplexerConfig] = []
        self._define_existing_resources()
        self._define_multiplexer_configs()
        self._define_multiplexer()

    def _define_existing_resources(self) -> None:
        self.existing_resources = self.existing_resources_class(
            self,
            'ExistingResources',
        )

    def _get_postgres_config(self, instance: Dict[str, Any]) -> PostgresConfig:
        return PostgresConfig(
            **instance
        )

    def _get_postgres_props(self, postgres_config: PostgresConfig) -> PostgresProps:
        return PostgresProps(
            **postgres_config.props,
            config=self.config,
            existing_resources=self.existing_resources,
        )

    def _define_multiplexer_configs(self) -> None:
        for instance in self.config.postgres['instances']:
            postgres_config = self._get_postgres_config(instance)
            postgres_props = self._get_postgres_props(postgres_config)
            postgres_class = postgres_factory(postgres_props)
            multiplexer_config = map_postgres_to_multiplexer_config(
                postgres_config=postgres_config,
                postgres_props=postgres_props,
                postgres_class=postgres_class,
            )
            self.multiplexer_configs.append(multiplexer_config)

    def _define_multiplexer(self) -> None:
        self.multiplexer = Multiplexer(
            scope=self,
            configs=self.multiplexer_configs,
        )
