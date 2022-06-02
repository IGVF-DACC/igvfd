import pytest


def test_stages_dev_initialize_dev_stages(config):
    from aws_cdk import App
    from infrastructure.stages.dev import DevelopmentDeployStage
    app = App()
    dev_deploy_stage = DevelopmentDeployStage(
        app,
        'TestDevelopmentDeployStage',
        config=config,
    )
    cloud_assembly = dev_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestDevelopmentDeployStage-PostgresStack',
        'TestDevelopmentDeployStage-BackendStack',
    ]
