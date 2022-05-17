import pytest


def test_stages_dev_initialize_dev_stages():
    from aws_cdk import App
    from infrastructure.config import Config
    from infrastructure.stages.dev import DevelopmentDeployStage
    app = App()
    branch = 'some-branch'
    dev_deploy_stage = DevelopmentDeployStage(
        app,
        'TestDevelopmentDeployStage',
        branch=branch,
        config=Config(
            branch=branch,
            pipeline='XYZ',
        )
    )
    cloud_assembly = dev_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestDevelopmentDeployStage-PostgresStack',
        'TestDevelopmentDeployStage-BackendStack',
    ]
