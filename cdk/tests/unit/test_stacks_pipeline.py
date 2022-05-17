import pytest

import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


def test_stacks_pipeline_continuous_deployment_pipeline_stack_initialized():
    from infrastructure.constructs.existing import igvf_dev
    from infrastructure.config import Config
    app = core.App()
    stack = ContinuousDeploymentPipelineStack(
        app,
        'CDStack',
        branch='test-pipeline-branch',
        existing_resources_class=igvf_dev.Resources,
        config=Config(
            branch='test-pipeline-branch',
            pipeline='XYZ',
        ),
        env=igvf_dev.US_WEST_2,
    )
    template = assertions.Template.from_stack(stack)
    template.resource_count_is(
        'AWS::CodePipeline::Pipeline',
        1
    )
    code_pipeline_resource = template.find_resources(
        'AWS::CodePipeline::Pipeline'
    )
    stages = code_pipeline_resource.get(
        'ContinuousDeploymentPipelineCodePipeline06633FEF'
    ).get(
        'Properties'
    ).get(
        'Stages'
    )
    assert len(stages) == 6
