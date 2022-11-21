from aws_cdk import Stack

from constructs import Construct

from infrastructure.config import Config

from infrastructure.constructs.opensearch import Opensearch
from infrastructure.constructs.opensearch import OpensearchProps

from infrastructure.constructs.existing.types import ExistingResourcesClass

from typing import Any


class OpensearchStack(Stack):

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
        self.existing_resources = existing_resources_class(
            self,
            'ExistingResources',
        )
        self.opensearch = Opensearch(
            self,
            'Opensearch',
            props=OpensearchProps(
                **config.opensearch,
                config=config,
                existing_resources=self.existing_resources,
            )
        )
