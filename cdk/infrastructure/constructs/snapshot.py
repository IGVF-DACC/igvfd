from aws_cdk import Duration
from aws_cdk import CustomResource
from aws_cdk import CfnOutput

from constructs import Construct

from aws_cdk.custom_resources import Provider
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_logs import RetentionDays

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_iam import Role

from typing import Any
from typing import cast


class LatestSnapshotFromDB(Construct):

    get_latest_rds_snapshot_id: PythonFunction
    provider: Provider
    latest_snapshot: CustomResource
    arn: str

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            db_instance_identifier: str,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.get_latest_rds_snapshot_id = PythonFunction(
            self,
            'GetLatestRDSSnapshotID',
            entry='infrastructure/runtime/lambda/rds',
            runtime=Runtime.PYTHON_3_9,
            index='snapshot.py',
            handler='custom_resource_handler',
            timeout=Duration.seconds(60),
        )

        # Make mypy happy.
        lambda_role = cast(
            Role,
            self.get_latest_rds_snapshot_id.role
        )

        lambda_role.add_to_policy(
            PolicyStatement(
                actions=['rds:DescribeDBSnapshots'],
                resources=['*'],
            )
        )

        self.provider = Provider(
            self,
            'Provider',
            on_event_handler=self.get_latest_rds_snapshot_id,
            log_retention=RetentionDays.ONE_MONTH,
        )

        self.latest_snapshot = CustomResource(
            self,
            'LatestRDSSnapshopID',
            service_token=self.provider.service_token,
            properties={
                'db_instance_identifier': db_instance_identifier,
            }
        )

        self.arn = self.latest_snapshot.get_att_string(
            'DBSnapshotArn'
        )

        CfnOutput(
            self,
            'LatestDBSnapshotArn',
            value=self.arn,
        )
