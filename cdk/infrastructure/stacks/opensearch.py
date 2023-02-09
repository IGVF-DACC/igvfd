from aws_cdk import Stack

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.opensearch import Opensearch
from infrastructure.constructs.opensearch import OpensearchProps

from infrastructure.constructs.existing.types import ExistingResourcesClass

from infrastructure.multiplexer import MultiplexerConfig
from infrastructure.multiplexer import Multiplexer

from typing import Any
from typing import Dict
from typing import List
from typing import Type

from dataclasses import dataclass


@dataclass
class OpensearchConfig:
    construct_id: str
    on: bool
    props: Dict[str, Any]


class OpensearchStack(Stack):

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
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.multiplexer_configs: List[MultiplexerConfig] = []
        self._define_multiplexer_configs()
        self._define_multiplexer()

    def _get_opensearch_config(self, cluster: Dict[str, Any]) -> OpensearchConfig:
        return OpensearchConfig(
            **cluster
        )

    def _get_opensearch_props(self, opensearch_config: OpensearchConfig) -> OpensearchProps:
        return OpensearchProps(
            **opensearch_config.props,
            config=self.config,
            existing_resources=self.existing_resources,
        )

    def _define_multiplexer_configs(self) -> None:
        for cluster in self.config.opensearch['clusters']:
            opensearch_config = self._get_opensearch_config(
                cluster,
            )
            opensearch_props = self._get_opensearch_props(
                opensearch_config,
            )
            multiplexer_config = MultiplexerConfig(
                construct_id=opensearch_config.construct_id,
                on=opensearch_config.on,
                construct_class=Opensearch,
                kwargs={
                    'props': opensearch_props,
                }
            )
            self.multiplexer_configs.append(multiplexer_config)

    def _define_multiplexer(self) -> None:
        self.multiplexer = Multiplexer(
            scope=self,
            configs=self.multiplexer_configs,
        )
