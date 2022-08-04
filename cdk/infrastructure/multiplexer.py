from aws_cdk import Stack

from constructs import Construct

from typing import Any
from typing import Dict
from typing import List
from typing import Type

from dataclasses import dataclass


@dataclass
class MultiplexerConfig:
    construct_id: str
    on: bool
    construct_class: Type[Construct]
    kwargs: Dict[str, Any]


class Multiplexer:

    def __init__(
            self,
            scope: Construct,
            *,
            configs: List[MultiplexerConfig],
            **kwargs: Any,
    ) -> None:
        self.scope = scope
        self.configs = configs
        self.resources: Dict[str, Construct] = {}
        self.create_resources()

    def create_resources(self) -> None:
        for config in self.configs:
            if not config.on:
                continue
            construct = config.construct_class(
                self.scope,
                config.construct_id,
                **config.kwargs,
            )
            self.resources[config.construct_id] = construct
