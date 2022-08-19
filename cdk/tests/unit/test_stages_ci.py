import pytest


def test_stages_ci_initialize_ci_stage(config):
    from aws_cdk import Stage
    from aws_cdk import App
    from infrastructure.stages.ci import CIDeployStage
    app = App()
    ci_deploy_stage = CIDeployStage(
        app,
        'TestCIDeployStage',
        config=config,
    )
    cloud_assembly = ci_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestCIDeployStage-ContinuousIntegrationStack',
    ]
    stack = cloud_assembly.get_stack_by_name(
        'TestCIDeployStage-ContinuousIntegrationStack',
    )
    assert stack.tags == {
        'branch': 'some-branch',
        'project': 'igvfd',
        'test': 'tag'
    }
