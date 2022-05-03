import pytest

from aws_cdk.assertions import Template


def test_stages_ci_initialize_ci_stage():
    from aws_cdk import Stage
    from aws_cdk import App
    from infrastructure.stages.ci import CIDeployStage
    app = App()
    ci_deploy_stage = CIDeployStage(
        app,
        'TestCIDeployStage',
    )
    cloud_assembly = ci_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestCIDeployStage-ContinuousIntegrationStack',
    ]
