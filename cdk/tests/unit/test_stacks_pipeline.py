import pytest

import aws_cdk.assertions as assertions


def test_stacks_pipeline_continuous_deployment_pipeline_stack_initialized(pipeline_config):
    from aws_cdk import App
    from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    stack = ContinuousDeploymentPipelineStack(
        app,
        'CDStack',
        existing_resources_class=igvf_dev.Resources,
        config=pipeline_config,
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
        'ContinuousDeploymentPipeline56548CF3'
    ).get(
        'Properties'
    ).get(
        'Stages'
    )
    assert len(stages) == 6


def test_stacks_pipeline_production_deployment_pipeline_stack_initialized(production_pipeline_config):
    from aws_cdk import App
    from infrastructure.stacks.pipeline import ProductionDeploymentPipelineStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    stack = ProductionDeploymentPipelineStack(
        app,
        'ProductionDeploymentPipelineStack',
        existing_resources_class=igvf_dev.Resources,
        config=production_pipeline_config,
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
        'ProductionDeploymentPipelineE21CAFC5',
    ).get(
        'Properties'
    ).get(
        'Stages'
    )
    assert len(stages) == 6
