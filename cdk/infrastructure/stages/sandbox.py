import aws_cdk as cdk

from constructs import Construct

from typing import Any


class SandboxDeployStage(cdk.Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id,  **kwargs)
