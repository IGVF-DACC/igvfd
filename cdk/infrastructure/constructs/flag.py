import json

from aws_cdk import App
from aws_cdk import Stack

from aws_cdk.aws_appconfig import CfnApplication
from aws_cdk.aws_appconfig import CfnEnvironment
from aws_cdk.aws_appconfig import CfnConfigurationProfile
from aws_cdk.aws_appconfig import CfnDeploymentStrategy
from aws_cdk.aws_appconfig import CfnHostedConfigurationVersion
from aws_cdk.aws_appconfig import CfnDeployment

from constructs import Construct

from dataclasses import dataclass

from typing import Any
from typing import Dict


@dataclass
class FeatureFlagServiceProps:
    branch: str
    environment_name: str
    flags: Dict[str, bool]


class FeatureFlagService(Construct):

    props: FeatureFlagServiceProps
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
        self._define_application()
        self._define_environment()
        self._define_configuration_profile()
        self._define_deployment_strategy()
        self._define_raw_flags()
        self._define_configuration_version()
        self._define_deployment()

    def _define_application(self) -> None:
        self.application = CfnApplication(
            self,
            'Application',
            name=self.props.branch,
        )

    def _define_environment(self) -> None:
        self.environment = CfnEnvironment(
            self,
            'Environment',
            application_id=self.application.ref,
            name=self.props.environment_name,
        )

    def _define_configuration_profile(self) -> None:
        self.configuration_profile = CfnConfigurationProfile(
            self,
            'ConfigurationProfile',
            application_id=self.application.ref,
            location_uri='hosted',
            name=f'{self.props.branch}-{self.props.environment_name}-feature-flags',
            type='AWS.AppConfig.FeatureFlags',
        )

    def _define_deployment_strategy(self) -> None:
        self.deployment_strategy = CfnDeploymentStrategy(
            self,
            'DeploymentStrategy',
            name=f'{self.props.branch}-{self.props.environment_name}-deployment-strategy',
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
            latest_version_number=1,
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
