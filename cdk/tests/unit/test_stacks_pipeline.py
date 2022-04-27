import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


def test_stacks_pipeline_continuous_deployment_pipeline_stack_created():
    from infrastructure.constructs.existing import igvf_dev
    app = core.App()
    stack = ContinuousDeploymentPipelineStack(
        app,
        'CDStack',
        branch='test-pipeline-branch',
        existing_resources=igvf_dev.Resources,
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
        'ContinuousDeploymentPipelinetestpipelinebranchCodePipelineD2E84AAD'
    ).get(
        'Properties'
    ).get(
        'Stages'
    )
    assert len(stages) == 6
