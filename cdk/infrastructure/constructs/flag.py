import json

from aws_cdk import CustomResource
from aws_cdk import Duration

from aws_cdk.aws_appconfig import CfnApplication
from aws_cdk.aws_appconfig import CfnEnvironment
from aws_cdk.aws_appconfig import CfnConfigurationProfile
from aws_cdk.aws_appconfig import CfnDeploymentStrategy
from aws_cdk.aws_appconfig import CfnHostedConfigurationVersion
from aws_cdk.aws_appconfig import CfnDeployment

from aws_cdk.custom_resources import Provider

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_iam import Role

from aws_cdk.aws_lambda import Runtime

from aws_cdk.aws_lambda_python_alpha import PythonFunction

from aws_cdk.aws_logs import RetentionDays

from constructs import Construct

from dataclasses import dataclass

from infrastructure.config import Config

from typing import Any
from typing import Dict
from typing import cast


@dataclass
class FeatureFlagServiceProps:
    config: Config
    flags: Dict[str, bool]


class FeatureFlagService(Construct):

    props: FeatureFlagServiceProps
    name: str
    application: CfnApplication
    environment: CfnEnvironment
    configuration_profile: CfnConfigurationProfile
    deployment_strategy: CfnDeploymentStrategy
    raw_flags: str
    configuration_version: CfnHostedConfigurationVersion
    deployment: CfnDeployment

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: FeatureFlagServiceProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_name()
        self._define_application()
        self._define_environment()
        self._define_configuration_profile()
        self._define_deployment_strategy()
        self._define_raw_flags()
        self._define_configuration_version()
        self._define_deployment()
        self._define_configuration_version_cleaner()

    def _define_name(self) -> None:
        self.name = f'{self.props.config.common.project_name}-{self.props.config.branch}'

    def _define_application(self) -> None:
        self.application = CfnApplication(
            self,
            'Application',
            name=self.name,
        )

    def _define_environment(self) -> None:
        self.environment = CfnEnvironment(
            self,
            'Environment',
            application_id=self.application.ref,
            name=self.props.config.name,
        )

    def _define_configuration_profile(self) -> None:
        self.configuration_profile = CfnConfigurationProfile(
            self,
            'ConfigurationProfile',
            application_id=self.application.ref,
            location_uri='hosted',
            name=f'{self.name}-{self.props.config.name}-feature-flags',
            type='AWS.AppConfig.FeatureFlags',
        )

    def _define_deployment_strategy(self) -> None:
        self.deployment_strategy = CfnDeploymentStrategy(
            self,
            'DeploymentStrategy',
            name=f'{self.name}-{self.props.config.name}-deployment-strategy',
            deployment_duration_in_minutes=0,
            growth_factor=100,
            replicate_to='NONE',
        )

    def _define_raw_flags(self) -> None:
        self.raw_flags = json.dumps(
            {
                'version': '1',
                'flags': {
                    k: {
                        'name': k
                    }
                    for k, v in self.props.flags.items()
                },
                'values': {
                    k: {
                        'enabled': v
                    }
                    for k, v in self.props.flags.items()
                }
            }
        )

    def _define_configuration_version(self) -> None:
        self.configuration_version = CfnHostedConfigurationVersion(
            self,
            'HostedConfigurationVersion',
            application_id=self.application.ref,
            configuration_profile_id=self.configuration_profile.ref,
            content_type='application/json',
            content=self.raw_flags,
        )

    def _define_deployment(self) -> None:
        self.deployment = CfnDeployment(
            self,
            'Deployment',
            application_id=self.application.ref,
            configuration_profile_id=self.configuration_profile.ref,
            configuration_version=self.configuration_version.ref,
            deployment_strategy_id=self.deployment_strategy.ref,
            environment_id=self.environment.ref,
        )

    def _define_configuration_version_cleaner(self) -> None:
        # CloudFormation doesn't track new AppConfig HostedConfigurationVersions
        # when toggling AppConfig flags in console. This custom resource
        # deletes all of the configuration versions when the stack is deleted.
        # Otherwise the stack fails to delete.
        delete_all_hosted_configuration_versions_on_clean_up = PythonFunction(
            self,
            'DeleteAllHostedConfigurationVersionsOnCleanUp',
            entry='infrastructure/runtime/lambdas/flag',
            runtime=Runtime.PYTHON_3_11,
            index='main.py',
            handler='custom_resource_handler',
            timeout=Duration.seconds(60),
        )
        lambda_role = cast(
            Role,
            delete_all_hosted_configuration_versions_on_clean_up.role
        )
        lambda_role.add_to_policy(
            PolicyStatement(
                actions=[
                    'appconfig:ListHostedConfigurationVersions',
                    'appconfig:DeleteHostedConfigurationVersion',
                ],
                resources=['*'],
            )
        )
        provider = Provider(
            self,
            'Provider',
            on_event_handler=delete_all_hosted_configuration_versions_on_clean_up,
            log_retention=RetentionDays.ONE_MONTH,
        )
        CustomResource(
            self,
            'HostedConfigurationVersionCleaner',
            service_token=provider.service_token,
            properties={
                'application_id': self.application.ref,
                'configuration_profile_id': self.configuration_profile.ref,
            }
        )
