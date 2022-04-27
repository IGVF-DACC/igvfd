import aws_cdk as cdk

from constructs import Construct

from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import DockerCredential
from aws_cdk.pipelines import ManualApprovalStep
from aws_cdk.pipelines import ShellStep

from aws_cdk.aws_secretsmanager import Secret

from infrastructure.naming import prepend_branch_name
from infrastructure.naming import prepend_project_name
from infrastructure.stages.ci import CIDeployStage
from infrastructure.stages.prod import ProdDeployStage
from infrastructure.stages.test import TestDeployStage
from infrastructure.stages.dev import DevelopmentDeployStage


class ContinuousDeploymentPipeline(Construct):

    def __init__(self, scope, construct_id, github_repo, branch, existing_resources, chatbot, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        self._github_repo = github_repo
        self._branch = branch
        self._chatbot = chatbot
        self._existing_resources = existing_resources
        self._define_github_connection()
        self._define_cdk_synth_step()
        self._define_docker_hub_credentials()
        self._make_code_pipeline()
        self._add_tooling_wave()
        self._add_development_deploy_stage()
        # self._add_test_deploy_stage()
        # self._add_prod_deploy_stage()
        self._maybe_add_slack_notifications()

    def _define_github_connection(self):
        self._github = CodePipelineSource.connection(
            self._github_repo,
            self._branch,
            connection_arn=self._existing_resources.code_star_connection.arn
        )

    def _define_cdk_synth_step(self):
        self._synth = ShellStep(
            'SynthStep',
            input=self._github,
            env={
                'BRANCH': self._branch
            },
            commands=[
                'npm install -g aws-cdk@2.12.0',
                'cd ./cdk',
                'python -m venv .venv',
                '. .venv/bin/activate',
                'pip install -r requirements.txt -r requirements-dev.txt',
                'pytest',
                'cdk synth -v -c branch=$BRANCH',
            ],
            primary_output_directory='cdk/cdk.out',
        )

    def _define_docker_hub_credentials(self):
        self._docker_hub_credentials = self._existing_resources.docker_hub_credentials

    def _get_docker_credentials(self):
        return DockerCredential.docker_hub(
            self._docker_hub_credentials.secret,
            secret_username_field='DOCKER_USER',
            secret_password_field='DOCKER_SECRET',
        )

    def _make_code_pipeline(self):
        self._code_pipeline = CodePipeline(
            self,
            prepend_branch_name(
                self._branch,
                'CodePipeline',
            ),
            synth=self._synth,
            docker_credentials=[
                self._get_docker_credentials(),
            ]
        )

    def _add_tooling_wave(self):
        tooling_wave = self._code_pipeline.add_wave(
            'tooling'
        )
        ci_stage = CIDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self._branch,
                    'DeployContinuousIntegration'
                )
            )
        )
        tooling_wave.add_stage(
            ci_stage
        )

    def _add_development_deploy_stage(self):
        stage = DevelopmentDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self._branch,
                    'DeployDevelopment',
                )
            ),
            branch=self._branch,
        )
        self._code_pipeline.add_stage(
            stage,
        )

    def _add_test_deploy_stage(self):
        stage = TestDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self._branch,
                    'DeployTest',
                )
            )
        )
        self._code_pipeline.add_stage(
            stage,
            pre=[
                ManualApprovalStep(
                    'RunTestDeploy'
                )
            ]
        )

    def _add_prod_deploy_stage(self):
        stage = ProdDeployStage(
            self,
            prepend_project_name(
                prepend_branch_name(
                    self._branch,
                    'DeployProduction',
                )
            )
        )
        self._code_pipeline.add_stage(
            stage,
            pre=[
                ManualApprovalStep(
                    'RunProductionDeploy'
                )
            ]
        )

    def _get_underlying_pipeline(self):
        if getattr(self, '_pipeline', None) is None:
            # Can't modify high-level CodePipeline after build.
            self._code_pipeline.build_pipeline()
            # Low-level pipeline.
            self._pipeline = self._code_pipeline.pipeline
        return self._pipeline

    def _maybe_add_slack_notifications(self):
        if self._chatbot is not None:
            self._get_underlying_pipeline().notify_on_execution_state_change(
                'NotifySlack',
                self._chatbot,
            )
