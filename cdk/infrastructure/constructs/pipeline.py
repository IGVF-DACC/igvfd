from constructs import Construct

from aws_cdk import RemovalPolicy

from aws_cdk.aws_codepipeline import Pipeline

from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3 import BlockPublicAccess

from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import DockerCredential
from aws_cdk.pipelines import ManualApprovalStep
from aws_cdk.pipelines import ShellStep
from aws_cdk.pipelines import Wave

from infrastructure.config import Config
from infrastructure.config import PipelineConfig
from infrastructure.config import build_config_from_name

from infrastructure.naming import prepend_branch_name
from infrastructure.naming import prepend_project_name

from infrastructure.stages.ci import CIDeployStage
from infrastructure.stages.demo import DemoDeployStage
from infrastructure.stages.dev import DevelopmentDeployStage
from infrastructure.stages.staging import StagingDeployStage
from infrastructure.stages.sandbox import SandboxDeployStage
from infrastructure.stages.production import ProductionDeployStage

from infrastructure.constructs.existing.types import ExistingResources

from typing import Any

from dataclasses import dataclass


@dataclass
class BasicSelfUpdatingPipelineProps:
    config: PipelineConfig
    existing_resources: ExistingResources
    github_repo: str


class BasicSelfUpdatingPipeline(Construct):

    github: CodePipelineSource
    synth: ShellStep
    artifact_bucket: Bucket
    underlying_pipeline: Pipeline
    code_pipeline: CodePipeline
    pipeline: Pipeline

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: BasicSelfUpdatingPipelineProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_github_connection()
        self._define_cdk_synth_step()
        self._define_artifact_bucket()
        self._define_underlying_pipeline()
        self._make_code_pipeline()

    def _define_github_connection(self) -> None:
        self.github = CodePipelineSource.connection(
            self.props.github_repo,
            self.props.config.branch,
            connection_arn=self.props.existing_resources.code_star_connection.arn
        )

    def _define_cdk_synth_step(self) -> None:
        self.synth = ShellStep(
            'SynthStep',
            input=self.github,
            env={
                'CONFIG_NAME': self.props.config.name,
                'BRANCH': self.props.config.branch,
            },
            install_commands=[
                f'npm install -g aws-cdk@{self.props.config.common.aws_cdk_version}',
                'cd ./cdk',
                'python -m venv .venv',
                '. .venv/bin/activate',
                'pip install -r requirements.txt -r requirements-dev.txt',
            ],
            commands=[
                'pytest tests/',
                'cdk synth -v -c branch=$BRANCH -c config-name=$CONFIG_NAME',
            ],
            primary_output_directory='cdk/cdk.out',
        )

    def _get_docker_credentials(self) -> DockerCredential:
        return DockerCredential.docker_hub(
            self.props.existing_resources.docker_hub_credentials.secret,
            secret_username_field='DOCKER_USER',
            secret_password_field='DOCKER_SECRET',
        )

    def _define_artifact_bucket(self) -> None:
        self.artifact_bucket = Bucket(
            self,
            'ArtifactsBucket',
            block_public_access=BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _define_underlying_pipeline(self) -> None:
        self.underlying_pipeline = Pipeline(
            self,
            'Pipeline',
            restart_execution_on_update=True,
            artifact_bucket=self.artifact_bucket
        )

    def _make_code_pipeline(self) -> None:
        self.code_pipeline = CodePipeline(
            self,
            'CodePipeline',
            synth=self.synth,
            docker_credentials=[
                self._get_docker_credentials(),
            ],
            docker_enabled_for_synth=True,
            code_pipeline=self.underlying_pipeline,
        )

    def _get_underlying_pipeline(self) -> Pipeline:
        if getattr(self, 'pipeline', None) is None:
            # Can't modify high-level CodePipeline after build.
            self.code_pipeline.build_pipeline()
            # Low-level pipeline.
            self.pipeline = self.code_pipeline.pipeline
        return self.pipeline

    def _add_slack_notifications(self) -> None:
        self._get_underlying_pipeline().notify_on_execution_state_change(
            'NotifySlack',
            self.props.existing_resources.notification.encode_dcc_chatbot,
        )


ContinuousDeploymentPipelineProps = BasicSelfUpdatingPipelineProps


class ContinuousDeploymentPipeline(BasicSelfUpdatingPipeline):

    dev_config: Config

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: ContinuousDeploymentPipelineProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )
        self._define_dev_environment_config()
        self._add_tooling_wave()
        self._add_development_deploy_stage()
        self._add_slack_notifications()

    def _define_dev_environment_config(self) -> None:
        self.dev_config = build_config_from_name(
            'dev',
            branch=self.props.config.branch,
        )

    def _add_tooling_wave(self) -> None:
        tooling_wave = self.code_pipeline.add_wave(
            'tooling'
        )
        ci_stage = CIDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'DeployContinuousIntegration'
                )
            ),
            config=self.dev_config,
        )
        tooling_wave.add_stage(
            ci_stage
        )

    def _add_development_deploy_stage(self) -> None:
        stage = DevelopmentDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'DeployDevelopment',
                )
            ),
            config=self.dev_config,
        )
        self.code_pipeline.add_stage(
            stage,
        )


DemoDeploymentPipelineProps = BasicSelfUpdatingPipelineProps


class DemoDeploymentPipeline(BasicSelfUpdatingPipeline):

    demo_config: Config

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: DemoDeploymentPipelineProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )
        self._define_demo_environment_config()
        self._add_development_deploy_stage()
        self._add_slack_notifications()

    def _define_demo_environment_config(self) -> None:
        self.demo_config = build_config_from_name(
            'demo',
            branch=self.props.config.branch,
        )

    def _add_development_deploy_stage(self) -> None:
        stage = DemoDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'DeployDevelopment',
                )
            ),
            config=self.demo_config,
        )
        self.code_pipeline.add_stage(
            stage,
        )


ProductionDeploymentPipelineProps = BasicSelfUpdatingPipelineProps


class ProductionDeploymentPipeline(BasicSelfUpdatingPipeline):

    staging_config: Config
    sandbox_config: Config
    production_config: Config
    staging_stage: StagingDeployStage
    sandbox_stage: SandboxDeployStage
    production_stage: ProductionDeployStage
    production_deploy_wave: Wave

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: ProductionDeploymentPipelineProps,
            **kwargs: Any,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            props=props,
            **kwargs,
        )
        self._define_staging_config()
        self._define_sandbox_config()
        self._define_production_config()
        self._define_staging_stage()
        self._define_sandbox_stage()
        self._define_production_stage()
        self._add_staging_deploy_stage()
        self._add_production_deploy_wave()
        self._add_sandbox_stage_to_production_deploy_wave()
        self._add_production_stage_to_production_deploy_wave()
        self._add_slack_notifications()

    def _define_staging_config(self) -> None:
        self.staging_config = build_config_from_name(
            'staging',
            branch=self.props.config.branch,
        )

    def _define_sandbox_config(self) -> None:
        self.sandbox_config = build_config_from_name(
            'sandbox',
            branch=self.props.config.branch,
        )

    def _define_production_config(self) -> None:
        self.production_config = build_config_from_name(
            'production',
            branch=self.props.config.branch,
        )

    def _define_staging_stage(self) -> None:
        self.staging_stage = StagingDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'StagingDeployStage',
                )
            ),
            config=self.staging_config,
        )

    def _define_sandbox_stage(self) -> None:
        self.sandbox_stage = SandboxDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'SandboxDeployStage',
                )
            ),
            config=self.sandbox_config,
        )

    def _define_production_stage(self) -> None:
        self.production_stage = ProductionDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self.props.config.branch,
                    'ProductionDeployStage',
                )
            ),
            config=self.production_config,
        )

    def _add_staging_deploy_stage(self) -> None:
        self.code_pipeline.add_stage(
            self.staging_stage
        )

    def _add_production_deploy_wave(self) -> None:
        self.production_deploy_wave = self.code_pipeline.add_wave(
            'production_deploy_wave',
            pre=[
                ManualApprovalStep(
                    'ProductionDeploymentManualApprovalStep'
                )
            ]
        )

    def _add_sandbox_stage_to_production_deploy_wave(self) -> None:
        self.production_deploy_wave.add_stage(
            self.sandbox_stage
        )

    def _add_production_stage_to_production_deploy_wave(self) -> None:
        self.production_deploy_wave.add_stage(
            self.production_stage
        )
