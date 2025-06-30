from constructs import Construct

from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer

from aws_cdk.aws_wafv2 import CfnWebACLAssociation

from infrastructure.config import Config

from dataclasses import dataclass

from typing import Any


@dataclass
class WAFProps:
    enabled: bool
    arn: str
    alb: ApplicationLoadBalancer


class WAF(Construct):

    props: WAFProps

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: WAFProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._maybe_add_association()

    def _maybe_add_association(self) -> None:
        if self.props.enabled is not True:
            return
        if not self.props.arn:
            return
        CfnWebACLAssociation(
            self,
            'CfnWebACLAssociation',
            resource_arn=self.props.alb.load_balancer_arn,
            web_acl_arn=self.props.arn,
        )
