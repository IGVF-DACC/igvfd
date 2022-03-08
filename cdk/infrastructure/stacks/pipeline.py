import aws_cdk as cdk

from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import ManualApprovalStep
from aws_cdk.pipelines import ShellStep

from infrastructure.naming import prepend_branch_name
from infrastructure.stages.test import TestDeployStage
from infrastructure.stages.prod import ProdDeployStage


class ContinuousDeploymentPipelineStack(cdk.Stack):

    def __init__(self, scope, construct_id, chatbot=None, branch=None, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
        self._chatbot = chatbot
        self._branch = branch
        self._define_github_connection()
        self._define_cdk_synth_step()
        self._make_code_pipeline()
        self._add_test_deploy_stage()
        self._add_prod_deploy_stage()
        self._maybe_add_slack_notifications()

    def _define_github_connection(self):
        self._github = CodePipelineSource.connection(
            'igvf-dacc/igvfd',
            self._branch,
            connection_arn=(
                'arn:aws:codestar-connections:'
                'us-east-1:618537831167:'
                'connection/28ec4d05-97dd-4730-b41c-b3b698b2a485'
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
                'npm install -g aws-cdk',
                'cd ./cdk',
                'python -m pip install -r requirements.txt -r requirements-dev.txt',
                'pytest',
                'cdk synth -c branch=$BRANCH',
            ]
        )

    def _make_code_pipeline(self):
        self._code_pipeline = CodePipeline(
            self,
            prepend_branch_name(
                self._branch,
                'CodePipeline',
            ),
            synth=self._synth
        )

    def _add_test_deploy_stage(self):
        stage = TestDeployStage(
            self,
            'TestDeployStage',
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
            'ProdDeployStage',
        )
        self._code_pipeline.add_stage(
            stage,
            pre=[
                ManualApprovalStep(
                    'RunProdDeploy'
                )
            ]
        )

    def _get_underlying_pipeline(self):
        if getattr(self, '_pipeline', None) is None:
            # Can't modify high-level CodePipeline after build.
            self._code_pipeline.build_pipeline()
            #Low-level pipeline.
            self._pipeline = self._code_pipeline.pipeline
        return self._pipeline

    def _maybe_add_slack_notifications(self):
        if self._chatbot is not None:
            self._get_underlying_pipeline().notify_on_execution_state_change(
                'NotifySlack',
                self._chatbot,
            )
