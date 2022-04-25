import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stacks.pipeline import ContinuousDeploymentPipelineStack


def test_stacks_pipeline_continuous_deployment_pipeline_stack_created():
    from infrastructure.config import IGVF_DEV_US_WEST_2
    from infrastructure.constructs.existing import IgvfDevExistingResources
    app = core.App()
    stack = ContinuousDeploymentPipelineStack(
        app,
        'CDStack',
        branch='test-pipeline-branch',
        existing_construct=IgvfDevExistingResources,
        env=IGVF_DEV_US_WEST_2,
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
        'testpipelinebranchCodePipelineBB1A604B'
    ).get(
        'Properties'
    ).get(
        'Stages'
    )
    assert len(stages) == 6
