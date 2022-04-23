import aws_cdk as cdk

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


class ContinuousDeploymentPipelineStack(cdk.Stack):

    def __init__(self, scope, construct_id, chatbot=None, branch=None, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        self._chatbot = chatbot
        self._branch = branch
        self._define_github_connection()
        self._define_cdk_synth_step()
        self._define_docker_credentials()
        self._make_code_pipeline()
        self._add_tooling_wave()
        self._add_development_deploy_stage()
        # self._add_test_deploy_stage()
        # self._add_prod_deploy_stage()
        self._maybe_add_slack_notifications()

    def _define_github_connection(self):
        self._github = CodePipelineSource.connection(
            'IGVF-DACC/igvfd',
            self._branch,
            connection_arn=(
                'arn:aws:codestar-connections:'
                'us-west-2:109189702753:'
                'connection/d65802e7-37d9-4be6-bc86-f94b2104b5ff'
            )
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

    def _define_docker_credentials(self):
        self._docker_credentials = Secret.from_secret_complete_arn(
            self,
            'DockerSecret',
            'arn:aws:secretsmanager:us-west-2:109189702753:secret:docker-hub-credentials-EStRH5',
        )

    def _get_docker_credentials(self):
        return DockerCredential.docker_hub(
            self._docker_credentials,
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
